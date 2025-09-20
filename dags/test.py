from airflow.decorators import dag, task
import pandas as pd
import polars as pl
import io


@dag(
    dag_id="test_dag",
    max_active_tasks=1,
    max_active_runs=1,
    tags=["example"],
)
def test_dag():
    @task
    def pass_pandas_df_in_xcom() -> pd.DataFrame:
        df = pd.DataFrame(data={"a": [i for i in range(50)]})
        print(df.describe())
        return df

    @task
    def recieve_pandas_df_xcom(data: pd.DataFrame):
        print(data.describe())

    @task
    def pass_polars_df_in_xcom() -> str:
        df = pl.DataFrame(data={"a": [i for i in range(50)]})
        print(df.describe())
        return df.write_json()

    @task
    def recieve_polars_df_xcom(data_json: str):
        data = pl.read_json(io.StringIO(data_json))
        print(data.describe())

    pd_df = pass_pandas_df_in_xcom()
    recieve_pandas_df_xcom(pd_df)

    pl_df = pass_polars_df_in_xcom()
    recieve_polars_df_xcom(pl_df)

    pd_df >> pl_df


test_dag()
