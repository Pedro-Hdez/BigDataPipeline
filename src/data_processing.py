from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

import time

# Kafka constants
KAFKA_TOPIC_NAME = 'ecommercetopic'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

# MySQL constants
MYSQL_HOST_NAME='localhost'
MYSQL_PORT='3306'
MYSQL_DATABASE='ecommerce'
MYSQL_TABLE='operations'
MYSQL_USR_NAME='admin'
MYSQL_PASSWORD='Admin123.,'
MYSQL_JDBC_URL=f'jdbc:mysql://{MYSQL_HOST_NAME}:{MYSQL_PORT}/{MYSQL_DATABASE}'

# Cassandra Constants
CASSANDRA_HOST_NAME = 'localhost'
CASSANDRA_PORT = '9042'
CASSANDRA_KEYSPACE='ecommerce_ks'
CASSANDRA_TABLE = 'operations'

def save_to_cassandra(current_df, epoc_id):
    print('Epoch id:', epoc_id)

    current_df \
        .write \
        .format('org.apache.spark.sql.cassandra') \
        .mode('append') \
        .options(table=CASSANDRA_TABLE, keyspace=CASSANDRA_KEYSPACE) \
        .save()

if __name__ == '__main__':
    print('Data Processing application started')
    print(time.strftime("%Y-%m-%d %H:%M:%S"))

    # Creating a Spark Session
    spark = SparkSession \
            .builder \
            .appName('Pyspark structured streaming') \
            .master('local[*]') \
            .getOrCreate()
    spark.sparkContext.setLogLevel('ERROR')

    # Extracting information from Kafka topic
    kafka_stream = spark \
        .readStream \
        .format('kafka') \
        .option('kafka.bootstrap.servers', KAFKA_BOOTSTRAP_SERVERS) \
        .option('subscribe', KAFKA_TOPIC_NAME) \
        .option('startingOffsets', 'latest') \
        .load()
    raw_info = kafka_stream.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

    # Building a Schema (columns and their types) to the information
    # retrieved
    df_schema = StructType() \
            .add('id', StringType()) \
            .add('event_time', StringType()) \
            .add('event_type', StringType()) \
            .add('product_id', StringType()) \
            .add('category_id', StringType()) \
            .add('category_code', StringType()) \
            .add('brand', StringType()) \
            .add('price', FloatType()) \
            .add('user_id', StringType()) \
            .add('user_session', StringType())
    
    # Application of the schema to the information retrieved
    df_raw = raw_info \
        .select(from_json(col('value'), df_schema).alias('dataframe'))
    df_raw = df_raw.select('dataframe.*')

    # Storing raw data into Cassandra database
    df_raw \
        .writeStream \
        .trigger(processingTime='15 seconds') \
        .outputMode('update') \
        .foreachBatch(save_to_cassandra) \
        .start()
    
    # Printing information retrieved to console
    df_output = df_raw \
        .writeStream \
        .trigger(processingTime='15 seconds') \
        .outputMode('update') \
        .option('truncate', 'false') \
        .format('console') \
        .start()

    df_output.awaitTermination()

