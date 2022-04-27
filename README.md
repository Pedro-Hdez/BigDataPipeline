# Big Data Pipeline

Este repositorio contiene el código fuente del proyecto final de la materia de Big Data de la [Maestría en Ciencia de Datos de la Universidad de Sonora](https://mcd.unison.mx/).

El objetivo del proyecto es la creación de un pipeline de Big Data utilizando herramientas optimizadas (y libres) para el manejo de grandes volúmenes de datos en tiempo real. Esta misma arquitectura podría replicarse, con sus respectivos ajustes, para atacar problemas de naturaleza similar. Los datos se obtendrán utilizando Apache Kafka; el procesamiento se realizará con Spark; después, el almacenamiento se realizará en dos formas: los datos crudos se cargarán a una base de datos NoSQL con Apache Cassandra y la información procesada se va a guardar en una base de datos SQL utilizando el gestor de base de datos MySQL dentro de un data warehouse montado sobre Apache Hive; finalmente, se creará un dashboard sencillo con Apache Superset. 

Para la simulación de un flujo de datos en tiempo real se utilizará la información correspondiente al mes de noviembre del 2020 del conjunto de datos de Kaggle [eCommerce behavior data from multi category store](https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store?select=2019-Nov.csv).
