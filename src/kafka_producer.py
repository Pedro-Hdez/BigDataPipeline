from kafka import KafkaProducer
import json
import pandas as pd
from random import randint
import time
import uuid

# Constants
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_TOPIC_NAME = 'ecommercetopic'
DATA_PATH = '/mnt/d/Users/pedro/Documents/mcd/2do_semestre/bigData/BigDataProject/data/2019-Nov.csv.zip'

# Serializer method
def serializer(data):
    return json.dumps(data).encode('utf-8')

# Producer object
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=serializer
)

# Dataframe to simulate real-time data flow
df = pd.read_csv(DATA_PATH, nrows=1000)
df['id'] = df.apply(lambda x: str(uuid.uuid1()), axis=1)

if __name__ == '__main__':
    while True:
        # Number of messages to send in this iteration
        n_msjs = randint(1, 5)
        # Getting random n_msjs from the dataframe
        sample_df = df.sample(n_msjs, axis=0)
        # Setting a timestamp
        sample_df.event_time = pd.Timestamp.now()
        sample_df.event_time = sample_df.event_time.astype('str')
        # Creating a list of dictionaries from sampled dataframe
        sample = sample_df.to_dict('records')

        # Sending all messages in the sample to Kafka Topic
        for message in sample:
            print(message)
            producer.send(KAFKA_TOPIC_NAME, message)
        # Sleep randomly between 1 and 3 seconds
        time.sleep(randint(1, 3))
