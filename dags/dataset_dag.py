import datetime
import os

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator,
    BigQueryDeleteDatasetOperator,
    BigQueryGetDatasetOperator,
    BigQueryUpdateDatasetOperator,
    BigQueryCreateEmptyTableOperator,
    BigQueryInsertJobOperator
)

DATASET_NAME = "darl_dataset_test"
TABLE_NAME = "darl_test_table"
DAG_ID = "BigQueryWorkflow"

with DAG(
    dag_id=DAG_ID,
    schedule_interval="@once",
    start_date=datetime.datetime(2023,10,23),
    catchup=False,
    tags=["BigQuery"],
) as dag:
    
    #1st step create the dataset that will be used to work
    create_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id="Create_Dataset",
        dataset_id=DATASET_NAME,
        #gcp_conn_id="Bq"
    )

    #2nd step update the dataset
    update_dataset =  BigQueryUpdateDatasetOperator(
        task_id = "Update_dataset",
        dataset_id=DATASET_NAME,
        dataset_resource={"description": "Dataset being updated from airflow step."},
        depends_on_past=True,
        #gcp_conn_id="Bq"
    )

    #3rd step getting dataset from BQ
    get_dataset = BigQueryGetDatasetOperator(
        task_id = "Get_dataset",
        dataset_id=DATASET_NAME,
        depends_on_past=True,
        #gcp_conn_id="Bq"
    )

    #4th step creating an empty table
    create_table = BigQueryCreateEmptyTableOperator(
        task_id="create_table",
        dataset_id=DATASET_NAME,
        table_id=TABLE_NAME,
        schema_fields=[
            {"name": "emp_name", "type": "STRING", "mode": "REQUIRED"},
            {"name": "salary", "type": "INTEGER", "mode": "NULLABLE"},
        ],
        depends_on_past=True,
    )

    #5th step inserting random data to a table
    INSERT_ROWS_QUERY = (
        f"INSERT {DATASET_NAME}.{TABLE_NAME} VALUES "
        f"('Diego',2500), "
        f"('Pepe',4350);"
    )

    insert_query_job = BigQueryInsertJobOperator(
        task_id="insert_query_job",
        configuration={
            "query": {
                "query": INSERT_ROWS_QUERY,
                "useLegacySql": False,
                "priority": "BATCH",
            }
        },
        location='US',
        depends_on_past=True,
    )

    #6th step BashOperator to wait until deletion of Dataset
    get_dataset_result = BashOperator(
        task_id = "Get_dataset_result",
        bash_command="sleep 60",
        depends_on_past=True,
    )

    #7th step deleting dataset
    delete_dataset = BigQueryDeleteDatasetOperator(
        task_id="Delete_dataset", 
        dataset_id=DATASET_NAME, 
        delete_contents=True,
        depends_on_past=True,
        #gcp_conn_id="Bq"
    )

    create_dataset >> update_dataset >> get_dataset >> create_table >> insert_query_job >> get_dataset_result >> delete_dataset