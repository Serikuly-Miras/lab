import polars as pl
from airflow.sdk import dag, task
from airflow.sdk.bases.hook import BaseHook


@dag(
    dag_id="test_postgres",
    tags=["test"],
)
def test_dag():
    @task
    def read_some() -> None:
        df = pl.read_database_uri(
            query="SELECT 1 as test;",
            uri=BaseHook.get_connection("dwh").get_uri(),
        )
        print(df)

    read_some()


test_dag()
