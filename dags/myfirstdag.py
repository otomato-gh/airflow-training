from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from textwrap import dedent
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
    templated_command = dedent(
    """
    {% for i in range(5) %}
      echo "{{ ds }}" #a variable (datestamp)
      echo "{{ macros.ds_add(ds, 7)}}" #a built-in macro
    {% endfor %}
    """
    )  

    t3 = BashOperator(
      task_id="templated",
      depends_on_past=False,
      bash_command=templated_command,
    )

    t2 >> t3

