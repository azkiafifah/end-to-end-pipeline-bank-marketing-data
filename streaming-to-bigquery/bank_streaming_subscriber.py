from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import csv
import json
import os
from time import sleep
from confluent_kafka import avro

# TODO(developer)
credentials = 'google_credentials.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials
project_id = "firm-pentameter-363006"
subscription_id = "bank_streaming"
# Number of seconds the subscriber should listen for messages
# timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = 'projects/firm-pentameter-363006/subscriptions/bank_streaming'

def send_record():
     file = open('data/bank_marketing_clean.csv')
     csvreader = csv.reader(file)
     header = next(csvreader)
     for row in csvreader:
         attributes =  {"age": int(row[0]), "job": str(row[1]), "marital": str(row[2]), "education": str(row[3]), "defaultloan": str(row[4]), "housingloan": str(row[5]), "loan": str(row[6])}
         try:
             attributes_dumped = json.dumps(attributes)
             streaming_pull_future = subscriber.subscribe(subscription_path, attributes_dumped.encode("utf-8"))
         except Exception as e:
             print(f"Exception while producing record value - {attributes}: {e}")
         else:
             print(f"Successfully producing record value - {attributes}")

         print(f'published message id {streaming_pull_future.result()}')
         sleep(1)

if __name__ == "__main__":
     send_record()

# def callback(message: pubsub_v1.subscriber.message.Message) -> None:
#     print(f"Received {message}.")
#     message.ack()

# streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
# print(f"Listening for messages on {subscription_path}..\n")

# # Wrap subscriber in a 'with' block to automatically call close() when done.
# with subscriber:
#     try:
#         # When `timeout` is not set, result() will block indefinitely,
#         # unless an exception is encountered first.
#         streaming_pull_future.result(timeout=timeout)
#     except TimeoutError:
#         streaming_pull_future.cancel()  # Trigger the shutdown.
#         streaming_pull_future.result()  # Block until the shutdown is complete.