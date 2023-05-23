import pytest
from airflow.models import DagBag
import collections

@pytest.fixture(scope="class")
def dag(dagbag):
    return dagbag.get_dag('forex_data_pipeline6')

class TestDagDefiniton:

    EXPECTED_TASK = 6
    EXPECTED_TASKS = ['print_date', 'print_something', 'task_3', 'task_4', 'task_5', 'func']

    compare = lambda self, x, y: collections.Counter(x) == collections.Counter(y)

    def test_tasks(self, dag):

        """
            Verify the number of tasks in the DAG
        """
        nb_tasks = len(dag.tasks)
        assert nb_tasks == self.EXPECTED_TASK, f"Wrong number of task, {self.EXPECTED_TASK} expected \
                                            {nb_tasks} got"
        
    def test_contain_tasks(self, dag):
        """
            Verify if correct id name is provided
        """

        task_id = list(map(lambda t: t.task_id, dag.tasks))
        assert self.compare(task_id, self.EXPECTED_TASKS)

    @pytest.mark.parametrize("task, expected_upstream, expected_downstream",
                             [
                            ("print_date", [], ["print_something"]), 
                            ("print_something", ["print_date"], ["task_3", "task_4", "task_5"]), 
                            ("task_3", ["print_something"], ["func"])
                             ]
                             )
    def test_dependencies_of_tasks(self, dag, task, expected_upstream, expected_downstream):

        task = dag.get_task(task)
        assert self.compare(task.upstream_task_ids, expected_upstream), "The task {0} doesn't have the expected upstream dependencies".format(task)
        assert self.compare(task.downstream_task_ids, expected_downstream), "The task {0} doesn't have the expected downstream dependencies".format(task)
