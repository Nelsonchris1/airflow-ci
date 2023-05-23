import pytest
from airflow.models import DagBag
import datetime

class TestDagValidation:

    LOAD_SECOND_THRESHOLD = datetime.timedelta(seconds=2)
    REQUIRED_EMAIL = "ogbeide331@gmail.com"
    EXPECTED_NUMBER_OF_DAGS = 1

    def test_import_dags(self, dagbag):
        """
            VERIFY THAT AIRLFOW IS ABLE TO IMPORT IN THE REPO
            - CHECK FOR TYPOS
            - CHECK FOR CYCLES
        """

        assert len(dagbag.import_errors) == 0, "DAG failures detected!  Got: {}".format(
            dagbag.import_errors
        )

    def test_time_import_dags(self, dagbag):
        """
            Verify that DAGsn load fast enough
            - check for loading time
        """
        stats = dagbag.dagbag_stats
        slow_dags = list(filter(lambda f: f.duration > self.LOAD_SECOND_THRESHOLD, stats))
        res = ', '.join(map(lambda f: f.file[1:], slow_dags))

        assert len(slow_dags) == 0, "The following DAGs take more than {0}s to load: {1}".format(
            self.LOAD_SECOND_THRESHOLD,
            res
        )

    #@pytest.mark.skip(reason="not yet added to DAGs")
    def test_default_args_email(self, dagbag):
        """
            Verify that Dags have the required email
            - check email
        """

        for dag_id, dag in dagbag.dags.items():
            emails = dag.default_args.get('emails', [])
            assert self.REQUIRED_EMAIL in emails, "The mail {0} for sending alerts is missing from \
                            thr DAG {1}".format(self.REQUIRED_EMAIL, dag_id)
            
    def test_default_args_retries(self, dagbag):
        """
            Verify that Dags have the correct retry
        """

        for dag_id, dag in dagbag.dags.items():
            retries = dag.default_args.get('retries', '')
            assert retries > 0 or retries == 2, f" {dag_id} uses a Wrong retry: {0}"
    
    def test_default_args_retries_delay(Self, dagbag):
        """
            Verify that Dags have the correct retry
        """

        for dag_id, dag in dagbag.dags.items():
            retry_delay = dag.default_args.get('retry_delay', '')
            assert retry_delay == datetime.timedelta(minutes=1), f" {dag_id} uses a Wrong retry_delay: {0}"



    def test_number_of_dags(self, dagbag):
        """
            Veritfy if ther number of dags in the dag folder is correct
        """

        stats = dagbag.dagbag_stats
        dag_num = sum([o.dag_num for o in stats])
        assert dag_num == self.EXPECTED_NUMBER_OF_DAGS, "Wrong number of dags, {0} expected got {1}".format(
            self.EXPECTED_NUMBER_OF_DAGS, dag_num
        )

    