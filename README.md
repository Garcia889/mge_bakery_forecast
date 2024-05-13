# Proyecto bakery forecast 💰

# (MCD ITAM Primavera 2024)


## Autores 📚

| Nombre                     |  CU    | Correo Electrónico | Usuario Github |
|----------------------------|--------|--------------------|----------------|
| Blanca E. García Manjarrez | 118886 | bgarci11@itam.mx   |    BGARCIAMA   |
| Iván García Alba           | 214549 | rgarc199@itam.mx   |    GARCIA889   |
| Valeria Durán Rubio        | 124273 | vduranru@itam.mx   |    VDR90       |
| Yuneri Pérez Arellano      | 199813 | yperezar@itam.mx   |    YunPerez    |



# Contexto  🧠
* Repositorio del proyecto de ...

* Blabla ...

# Objetivo del proyecto  🎯
* Utilizar tecnologías de gran escala...

## Habilidades a evaluar 🧑‍💻
* Bla...

# Base de datos  ✍
* ...
* Los dataset que se analizaron van del...

# Estructura del Proyecto
## Parte A 📑
* En esta parte se levantó un cluster en AWS con Hadoop y Pyspark 

* Elaboramos un ETL con el Cluster donde: 
* - Se subió a S3 el archivo o archivos.
* - Se cargó el CSV en Spark.
* - Se guardó el CSV como parquet en S3, y se particionó por `catalogo` y `año`.
* - Se cargó el parquet en Spark.
* - Y se hizó el análisis solicitado en las instrucciones [instrucciones-proyecto-parcial.md](instrucciones-proyecto-parcial.md).
 
## Parte B 📑
Para esta parte se utilizó **Athena**. 

* - Se creó una base de datos `profeco_db` en Athena.
* - Así como una tabla externa `profeco` dentro de la base de datos profeco_db.

## Requerimientos de Software herramientas recomendadas

1. [Cuenta de Github](https://github.com)
2. [VSCodeIDE](https://code.visualstudio.com)
3. [AWS](https://aws.amazon.com)


- Correr los scripts en el siguiente orden:
  1. [0.WebScrapping.ipynb](0.WebScrapping.ipynb) 
  2. [bash/1.limpieza.sh](bash/1.limpieza.sh)
  3. [bash/2.union.sh](bash/2.union.sh)
  4. [3.Parte_A.ipynb](3.Parte_A.ipynb)
  5. [4.Parquet_basicos.ipynb](4.Parquet_basicos.ipynb)
  6. [5.Parte_B.ipynb](5.Parte_B.ipynb)

# Entregables 💯




