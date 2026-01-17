from airflow.decorators import dag, task


@dag(
    dag_id="setup_s3_buckets",
    tags=["s3", "workload"],
)
def test_dag():
    @task
    def create_buckets() -> None:
        pass

    @task
    def setup_airflow_lifetime_policy() -> None:
        pass

    create_buckets()
    setup_airflow_lifetime_policy()


test_dag()
