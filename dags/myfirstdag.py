from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
with DAG(
    'first',
    start_date=days_ago(0),
    description='Our first little DAG',
    tags=['first']
) as dag:
    t1 = BashOperator(
        task_id='show_date',
        bash_command='date',
    )
    t2 = BashOperator(
        task_id='show_host',
        bash_command='hostname',
    )

    t2 >> t1
