from airflow.models import DAG
from airflow.operators.empty import EmptyOperator


def factory_subdag(parent_dag_name, child_dag_name, default_args):
    with DAG(
        dag_id=f"{parent_dag_name}.{child_dag_name}", default_args=default_args
    ) as dag:
        task_2 = EmptyOperator(task_id="task_10")

        task_3 = EmptyOperator(task_id="task_11")

    return dag
