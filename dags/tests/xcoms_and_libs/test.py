import base64
import io

import pandas as pd
import polars as pl
from airflow.decorators import dag, task


@dag(
    dag_id="test_dag",
    tags=["test"],
)
def test_dag():
    @task
    def pass_pandas_df_in_xcom() -> str:
        df = pd.DataFrame(data={"a": [i for i in range(50)]})
        print(df.describe())
        return base64.b64encode(df.to_parquet()).decode("utf-8")

    @task
    def recieve_pandas_df_xcom(data: str):
        data = pd.read_parquet(io.BytesIO(base64.b64decode(data)))
        print(data.describe())

    @task
    def pass_polars_df_in_xcom() -> str:
        df = pl.DataFrame(data={"a": [i for i in range(50)]})
        print(df.describe())
        return base64.b64encode(df.write_parquet()).decode("utf-8")

    @task
    def recieve_polars_df_xcom(data: str):
        data = pl.read_parquet(io.BytesIO(base64.b64decode(data)))
        print(data.describe())

    pd_df = pass_pandas_df_in_xcom()
    recieve_pandas_df_xcom(pd_df)

    pl_df = pass_polars_df_in_xcom()
    recieve_polars_df_xcom(pl_df)

    pd_df >> pl_df


test_dag()
