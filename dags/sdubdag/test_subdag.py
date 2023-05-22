# from airflow import DAG
# from airflow.operators.empty import EmptyOperator
# from airflow.utils.task_group import TaskGroup
# from airflow.operators.bash import BashOperator
# from functions.helpers import print_word, func
# from airflow.operators.python import PythonOperator
# from datetime import timedelta, datetime


# def func():
#     print("This was created by Nelson")

# default_args = {
#     "owner": "Nelson",
#     "email_on_failure": True,
#     "email_on_retry": True,
#     "retries": 2,
#     "retry_delay": timedelta(minutes=1),
# }

# with DAG(dag_id="task_group_dag", start_date=datetime(2023, 5, 2), schedule="@daily",
#          catchup=True, default_args=default_args) as dag:


#     t1 = BashOperator(
#         task_id = "print_date",
#         dag = dag,
#         bash_command= 'echo "The date is $(date)"',
#         wait_for_downstream=True
#     )

#     t2 = PythonOperator(
#         task_id='print_something',
#         python_callable=print_word,
#         dag=dag,
#         depends_on_past=True
#     )

#     with TaskGroup('processing_tasks') as processing_tasks:
#         task_3 = BashOperator(
#             task_id = "task3",
#             bash_command="echo God id good"
#         )

#         with TaskGroup('spark_task') as spark_tasks:
#             task_99 = EmptyOperator(
#                 task_id="realtime"
#             )


#         with TaskGroup('flink_task') as flink_tasks:
#             task_88 = EmptyOperator(
#                 task_id="realtime"
#             )

#         task_4 = BashOperator(
#             task_id= "task_4",
#             bash_command="echo All the time"
#         )

#     task_5 = EmptyOperator(
#         task_id="task_5"
#     )

# t1 >> t2 >> processing_tasks >> task_5
