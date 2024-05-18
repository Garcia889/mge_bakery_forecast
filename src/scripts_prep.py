'''
Este módulo es un script que provee
las funciones que se emplean en el
script de:
* Preprocesamiento de datos

El índice de las funciones es el siguiente:
* load_data
* day_time
* preprocess_data
'''
# Se importan las librerías necesarias
# pylint: disable = unused-import
import os
import warnings
import pandas as pd
import logging
from datetime import datetime

# Se configura el logging
if not os.path.exists("logs/"):
    os.makedirs("logs/")
# Setup Logging
now = datetime.now()
date_time = now.strftime("%Y%m%d_%H%M%S")
log_prep_file_name = f"logs/{date_time}_prep.log"
logging.basicConfig(
    filename=log_prep_file_name,
    level=logging.DEBUG,
    filemode='w',  # Cambiado de 'a' a 'w' para sobrescribir los logs
    format='%(name)s - %(levelname)s - %(message)s')

def load_data(data_bakery_sales):
    '''
    Esta función se encarga de cargar los datos
    de entrada en formato .csv que se encuentran
    en la carpeta data/raw y los devuelve en un
    DataFrame de pandas.

    Parameters:
    input_data (str): Ruta del archivo de
                            datos de entrada en formato .csv.

    Returns:
    data (DataFrame): DataFrame de pandas que contiene
                    los datos de entrada en formato .csv.
    '''
    try:
        # Leer datos de entrada .csv
        data = pd.read_csv(data_bakery_sales)
        # Se eliminan las columnas que contienen más del 60% de valores nulos
        data = data.drop_duplicates()
        logging.info(
            f"La base data_bakery_sales fue cargada correctamente")
        # Assert
        assert isinstance(data, pd.DataFrame)
        assert len(data) == len(pd.read_csv(data_bakery_sales))
        return data
    except (FileNotFoundError, pd.errors.EmptyDataError) as exc:
        print(f"Ocurrió un error con la lectura del archivo: {exc}")
        return None

def day_time (Day_time):
    """
    Esta función clasifica el tiempo del día en
    'Morning', 'Afternoon' y 'Evening' según la
    hora del día.
    """
    try:
        if Day_time < 12:
            return 'Morning'
        elif Day_time < 17:
            return 'Afternoon'
        else:
            return 'Evening'
    except Exception as e:
        logging.error(f"Error al clasificar el tiempo del día: {e}")
        return None

def preprocess_data(input_data, output_prep_data="data/prep/data_bakery_prep.csv"):
    """
    Preprocesa los datos de entrada imputando valores faltantes y
    seleccionando variables relevantes para el modelo.
    Parámetros:
    input_data (str): la ruta al archivo de datos de entrada en formato CSV.
    output_prep_data (str): la ruta para guardar los datos
    preprocesados en formato CSV. El valor predeterminado
    es "data/prep/data_prep.csv".
    Salida:
    pandas.DataFrame: los datos preprocesados con variables seleccionadas.
    """
    try:
        # Cargar datos desde el archivo CSV
        data = pd.read_csv(input_data)
        logging.info(f"Los datos fueron cargados correctamente desde {input_data}")
        # Renombra columnas
        df_raw = data.rename(columns={'date': 'Date',
                                      'time': 'Time',
                                      'ticket_number': 'Transaction_id',
                                      'article': 'Menu',
                                      'unit_price': 'Price'})
        # Convierte 'Menu' a mayúsculas y minúsculas
        df_raw['Menu'] = df_raw['Menu'].str.title()
        # Arregla formato de valores 'Quantity' y 'Price'
        df_raw = df_raw.replace(to_replace={'Quantity': {'.': ' '},  # np.NaN
                                            'Price': {'€': ' ', ',': '.'}}, regex=True)
        # Conversión de datos númericos
        df_raw = df_raw.astype({'Quantity': 'int',
                                'Price': 'float',
                                'Transaction_id': 'int',
                                'Menu': 'str'})
        warnings.filterwarnings('ignore')
        # Crea columna 'Revenue'
        df_raw['Revenue'] = df_raw['Quantity'] * df_raw['Price']
        # Cambia Date a datetime
        df_raw['Date'] = pd.to_datetime(df_raw['Date'])
        # Separa 'Date' en 'Week_day', 'Day', Month' y 'Year'
        df_raw['Week_day'] = df_raw['Date'].dt.weekday
        df_raw['Day'] = df_raw['Date'].dt.day
        df_raw['Year'] = df_raw['Date'].dt.year
        df_raw['Month'] = df_raw['Date'].dt.to_period('M')
        df_raw['Quarter'] = df_raw['Date'].dt.to_period('Q')
        # 'Week_day' en nombres de días y 'Month' a nombres de meses
        df_raw = df_raw.replace(to_replace={'Week_day': {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday',
                                                         3: 'Thursday', 4: 'Friday', 5: 'Saturday',
                                                         6: 'Sunday'}}, regex=True)
        # Separa 'Time' y la convierte en datetime
        df_raw['Day_time'] = pd.to_datetime(df_raw['Time']).dt.hour
        df_raw['Day_time'] = df_raw.Day_time.apply(day_time)
        # Ordena columnas para visualización
        df_raw.sort_values(by=['Menu', 'Quantity', 'Price', 'Revenue'])
        # Elimina valores '.' y 0 en 'Price'
        df_raw = df_raw[~df_raw['Menu'].isin(['.'])].reset_index(drop=True)
        df_raw = df_raw[~df_raw['Price'].isin([0])].reset_index(drop=True)
        # Elimina valores negativos
        df_raw = df_raw.loc[~((df_raw['Quantity'] <= 0)
                               | (df_raw['Revenue'] <= 0))].reset_index(drop=True)
        # Elimina outliers basado en EDA
        df_raw = df_raw.loc[~(df_raw['Revenue'] >= 100)].reset_index(drop=True)
        df_raw = df_raw.loc[~(df_raw['Quantity'] >= 100)].reset_index(drop=True)
        # Guardar el resultado en un nuevo archivo CSV
        df_raw.to_csv(output_prep_data, index=False)
        logging.info(
            f"Los datos fueron preprocesados y guardados en {output_prep_data}")
        return df_raw
    except Exception as e:
        logging.error(f"Error en el preprocesamiento de los datos: {e}")
        return None
