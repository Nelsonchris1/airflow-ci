from datetime import datetime, timedelta

from functions.helpers import func, print_word

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


def on_sucess_callback(dict):
    print(dict)


def on_failure_callback(dict):
    print(dict)


"""
Dag level :1) dagrun_timeout=(timedelta(seconds=30))
2) on_success_callback=on_success_callback -> function with dict parameter
3) on_failure_callback=on_failure_callback -> function with dict parameter
task level  :-> execution_timout =timedelta(seconds=60)
"""

default_args = {
    "owner": "Nelson",
    "emails": "ogbeide331@gmail.com",
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
    "on_failure_callback": on_failure_callback,
    "on_success_callback": on_sucess_callback,
}

with DAG(
    "forex_data_pipeline6",
    start_date=datetime(2023, 4, 29),
    schedule="@daily",
    catchup=True,
    default_args=default_args,
) as dag:
    t1 = BashOperator(
        task_id="print_date",
        dag=dag,
        bash_command='echo "The date is $(date)"',
        wait_for_downstream=True,
    )

    t2 = PythonOperator(
        task_id="print_something",
        python_callable=print_word,
        dag=dag,
        depends_on_past=True,
    )

    tasks = [EmptyOperator(task_id="task_{0}".format(t)) for t in range(3, 6)]

    t6 = PythonOperator(
        task_id="func", python_callable=func, dag=dag, depends_on_past=True
    )


t1 >> t2
t2 >> tasks
tasks >> t6
