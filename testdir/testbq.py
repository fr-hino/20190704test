from airflow.contrib.operators import bigquery_operator
from airflow import DAG
from airflow.utils.dates import days_ago
from datetime import timedelta

# Query recent StackOverflow questions.

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# dag = DAG("tableau_dags", default_args=default_args,schedule_interval='@daily', catchup=False)
dag = DAG("testbq", default_args=default_args,
          schedule_interval='0 10 * * * ', catchup=False)


bq_recent_questions_query = bigquery_operator.BigQueryOperator(
    task_id='bq_recent_questions_query',
    bigquery_conn_id='bigquery_default',
    sql="""
    SELECT * FROM `fr-stg-self-service-bi.sekitest.superstore_seki` LIMIT 500
    """,
    use_legacy_sql=False,
    destination_dataset_table='fr-stg-self-service-bi.sekitest.superstore_seki2',
    write_disposition='WRITE_TRUNCATE',
    dag=dag)

bq_recent_questions_query
