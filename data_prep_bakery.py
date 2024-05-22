"""
Este script se encarga de tomar los datos preprocesados
de ventas y clima, y realizar las siguientes tareas:
1. Unir los datos de ventas y clima.
2. Agrupar los datos por año, mes, día,
   temperatura promedio y código de menú.
3. Dividir los datos en conjuntos de entrenamiento,
   validación y prueba.
4. Guardar los conjuntos de datos en formato CSV.
5. Subir los archivos CSV a un bucket de S3.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
import boto3

# Leer datos de ventas en formato Parquet desde S3
BAKERY_DATA_PATH = 's3://smartbakery/clean_data/clean_bakery_sales.csv'
bakery_df = pd.read_csv(BAKERY_DATA_PATH)

# Convertir la columna 'Date' a formato datetime
bakery_df['Date'] = pd.to_datetime(bakery_df['Date'])
bakery_df['Month'] = bakery_df['Month'].str.replace('-', '')

# Convertir la columna 'Menu' a formato numerico
bakery_df['Menu_Code'] = pd.Categorical(bakery_df['Menu']).codes

# Crear un DataFrame con los códigos de menú
df_menu = bakery_df[['Menu_Code', 'Menu', 'Price']]
df_menu = df_menu.drop_duplicates(subset=['Menu_Code', 'Menu'])

# Leer datos de Temperatura
WEATHER_DATA_PATH = './raw_data/TempTot.csv'
weather_df = pd.read_csv(WEATHER_DATA_PATH)

# Convertir la columna 'Fecha' a formato datetime
weather_df['Fecha'] = pd.to_datetime(weather_df['Fecha'], format='%d/%m/%y')

# Unir los DataFrames de ventas y clima
df_joined = pd.merge(bakery_df,
                     weather_df, left_on='Date',
                     right_on='Fecha', how='left')

# Eliminar columnas innecesarias
df_joined = df_joined[[
    'Quantity', 'Year', 'Month', 'Day', 'Avg_temp', 'Menu_Code']]
df_grouped = df_joined.groupby(
    ['Year', 'Month', 'Day', 'Avg_temp', 'Menu_Code']
    ).agg({'Quantity': 'sum'}).reset_index()

# Reordenar las columnas
df_grouped = df_grouped[[
    'Quantity', 'Year', 'Month', 'Day', 'Avg_temp', 'Menu_Code'
     ]]

# Dividir el conjunto de datos en entrenamiento (80%) y prueba (20%)
train_df, test_df = train_test_split(
    df_grouped, test_size=0.2, random_state=42)

# Dividir datos en entrenamiento (70%) y validación (30%)
train_df, val_df = train_test_split(train_df, test_size=0.3, random_state=42)

# Imprimir la longitud de cada conjunto de datos
print("Tamaño del conjunto de entrenamiento:", len(train_df))
print("Tamaño del conjunto de validación:", len(val_df))
print("Tamaño del conjunto de prueba:", len(test_df))
print("Tamaño del conjunto de menú:", len(df_menu))

# Convertir los DataFrames a formato CSV
train_df.to_csv('train.csv', index=False)
val_df.to_csv('val.csv', index=False)
test_df.to_csv('test.csv', index=False)
df_menu.to_csv('menu_codes.csv', index=False)

# Establecer conexión con S3
s3 = boto3.client('s3',
                  aws_access_key_id='XXXXXXXX',
                  aws_secret_access_key='XXXXXXXXXX')

# Especificar el nombre del bucket de S3 y los nombres de los archivos
BUCKET_NAME = 'smartbakery'
TRAIN_FILE_KEY = 'clean_data/train.csv'
VAL_FILE_KEY = 'clean_data/validation.csv'
TEST_FILE_KEY = 'clean_data/test.csv'
MENU_CODES_KEY = 'clean_data/menu_codes.csv'

# Subir los archivos CSV a S3
s3.upload_file('train.csv', BUCKET_NAME, TRAIN_FILE_KEY)
s3.upload_file('val.csv', BUCKET_NAME, VAL_FILE_KEY)
s3.upload_file('test.csv', BUCKET_NAME, TEST_FILE_KEY)
s3.upload_file('menu_codes.csv', BUCKET_NAME, MENU_CODES_KEY)

print("Archivos CSV guardados en S3 exitosamente.")
