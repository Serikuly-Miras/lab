import polars as pl
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk import dag, task
from airflow.sdk.bases.hook import BaseHook


@dag(
    dag_id="test_postgres",
    tags=["test"],
)
def test_dag():
    @task
    def read_some_using_polars() -> None:
        c = BaseHook.get_connection("dwh")
        uri = f"postgresql://{c.login}:{c.password}@{c.host}:{c.port}/{c.schema}"  # noqa
        df = pl.read_database_uri(query="SELECT 1 as test;", uri=uri)
        print(df)

    read_some_using_operator = SQLExecuteQueryOperator(
        task_id="read_some_using_operator",
        conn_id="dwh",
        sql="SELECT 1 as test;",
    )

    read_some_using_polars
    read_some_using_operator


test_dag()
