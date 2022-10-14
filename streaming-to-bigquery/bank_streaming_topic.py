import csv
from time import sleep
import os
from google.cloud import pubsub_v1
import json
import base64
from confluent_kafka import avro
credentials = 'google_credentials.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials
publisher = pubsub_v1.PublisherClient()
topic_path = 'projects/firm-pentameter-363006/topics/bank_streaming'


def send_record():
     file = open('data/bank_marketing_clean.csv')
     csvreader = csv.reader(file)
     header = next(csvreader)
     for row in csvreader:
         attributes =  {"age": int(row[0]), "job": str(row[1]), "marital": str(row[2]), "education": str(row[3]), "defaultloan": str(row[4]), "housingloan": str(row[5]), "loan": str(row[6])}
         try:
             attributes_dumped = json.dumps(attributes)
             future = publisher.publish(topic_path, attributes_dumped.encode("utf-8"))
         except Exception as e:
             print(f"Exception while producing record value - {attributes}: {e}")
         else:
             print(f"Successfully producing record value - {attributes}")

         print(f'published message id {future.result()}')
         sleep(1)

if __name__ == "__main__":
     send_record()
