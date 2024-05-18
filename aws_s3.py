"""
El siguiente módulo manda los datos
preprocesados a un bucket de S3 en AWS
"""
# Se importan las librerías necesarias
# pylint: disable = unused-import
import os
import logging
from datetime import datetime
import pandas as pd
import boto3
from botocore.exceptions import (
    NoCredentialsError,
    PartialCredentialsError,
    ClientError)
# Se configura el logging
if not os.path.exists("logs/"):
    os.makedirs("logs/")
# Setup Logging
now = datetime.now()
date_time = now.strftime("%Y%m%d_%H%M%S")
log_prep_file_name = f"logs/{date_time}_s3.log"
logging.basicConfig(
    filename=log_prep_file_name,
    level=logging.DEBUG,
    filemode='w',  # Cambiado de 'a' a 'w' para sobrescribir los logs
    format='%(name)s - %(levelname)s - %(message)s')

try:
    # Credenciales de AWS
    VAR_KEY_ID = 'your_aws_access_key_id'
    VAR_ACCESS_KEY = 'your_aws_secret_access_key'
    logging.info("Credenciales de AWS cargadas correctamente")

    # Set the S3 bucket name and file name
    BUCKET_NAME = 'bakery-project'
    CSV_FILE_NAME = './data/prep/data_bakery_prep.csv'
    PARQUET_FILE_NAME = './clean_data/clean_bakery_sales.parquet'
    logging.info("Nombre del bucket y archivo definidos correctamente")

    # Read the CSV file
    df = pd.read_csv(CSV_FILE_NAME)
    logging.info("Archivo CSV %s cargado correctamente", CSV_FILE_NAME)

    # Convert the dataframe to Parquet format
    df.to_parquet(PARQUET_FILE_NAME)
    logging.info("Archivo Parquet %s creado correctamente", PARQUET_FILE_NAME)

    # Create an S3 client
    s3 = boto3.client('s3',
                      aws_access_key_id=VAR_KEY_ID,
                      aws_secret_access_key=VAR_ACCESS_KEY)
    logging.info("Cliente S3 creado correctamente")

    # Upload the Parquet file to S3
    s3.upload_file(PARQUET_FILE_NAME,
                   BUCKET_NAME, 'clean_bakery_sales.parquet')
    logging.info(
        "Archivo Parquet %s subido correctamente a S3 en %s",
        PARQUET_FILE_NAME, BUCKET_NAME)

except FileNotFoundError as e:
    logging.error("Archivo no encontrado: %s", e)
except pd.errors.EmptyDataError as e:
    logging.error("Archivo CSV vacío: %s", e)
except NoCredentialsError as e:
    logging.error("Error de credenciales: %s", e)
except PartialCredentialsError as e:
    logging.error("Credenciales incompletas: %s", e)
except ClientError as e:
    logging.error("Error del cliente de AWS: %s", e)
