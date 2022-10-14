import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator


PROJECT_ID = "firm-pentameter-363006"
BUCKET = "wfwijaya-fellowship"

dataset = "bank_marketing"
dataset_file = "bank-marketing.csv"
dataset_url = f"https://storage.googleapis.com/wfwijaya-fellowship/{dataset_file}"

# path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
path_to_local_home = "/home/airflow"
BIGQUERY_DATASET = os.environ.get("bank_marketing", 'bank_marketing')

def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client(project ='firm-pentameter-363006')
    bucket = client.bucket(BUCKET)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="batch_data",
    schedule_interval="@weekly",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:

    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"curl -sSL {dataset_url} > {path_to_local_home}/{dataset_file}"
    )

    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"data/{dataset_file}",
            "local_file": f"{path_to_local_home}/{dataset_file}",
        },
    )

    # You have to create bigquery project and bigquery dataset before you run this task
    GCStoBQ = GCSToBigQueryOperator(
         task_id="GCStoBQ_task",
         bucket = 'wfwijaya-fellowship',
         source_objects= f"data/{dataset_file}",
         destination_project_dataset_table=  "{}.{}.{}".format(PROJECT_ID,dataset,dataset),
         skip_leading_rows = 1,
         schema_fields = [{"name": "age", "type": "INTEGER", "mode": "NULLABLE"},
               {"name": "job", "type": "STRING", "mode": "NULLABLE"},
               {"name": "marital", "type": "STRING", "mode": "NULLABLE"},
               {"name": "education", "type": "STRING", "mode": "NULLABLE"},
               {"name": "defaultloan", "type": "STRING", "mode": "NULLABLE"},
               {"name": "housingloan", "type": "STRING", "mode": "NULLABLE"},
               {"name": "loan", "type": "STRING", "mode": "NULLABLE"},
               {"name": "contact", "type": "STRING", "mode": "NULLABLE"},
               {"name": "month", "type": "STRING", "mode": "NULLABLE"},
               {"name": "day_of_week", "type": "STRING", "mode": "NULLABLE"},
               {"name": "duration", "type": "INTEGER", "mode": "NULLABLE"},
               {"name": "campaign", "type": "INTEGER", "mode": "NULLABLE"},
               {"name": "pdays", "type": "INTEGER", "mode": "NULLABLE"},
               {"name": "previous", "type": "INTEGER", "mode": "NULLABLE"},
               {"name": "poutcome", "type": "STRING", "mode": "NULLABLE"},
               {"name": "empvarrate", "type": "FLOAT", "mode": "NULLABLE"},
               {"name": "conspriceidx", "type": "FLOAT", "mode": "NULLABLE"},
               {"name": "consconfidx", "type": "FLOAT", "mode": "NULLABLE"},
               {"name": "euribor3m", "type": "FLOAT", "mode": "NULLABLE"},
               {"name": "nremployed", "type": "FLOAT", "mode": "NULLABLE"},
               {"name": "y", "type": "STRING", "mode": "NULLABLE"}
               ]
    )

    download_dataset_task >> local_to_gcs_task  >> GCStoBQ