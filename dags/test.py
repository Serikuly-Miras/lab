from airflow.decorators import dag, task


@dag(
    dag_id="test_dag",
    start_date=None,
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["example"],
    default_args={},
)
def test_dag():
    @task
    def test() -> None:
        print("testing dag")

    test()


test_dag()
