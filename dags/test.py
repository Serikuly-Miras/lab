from airflow.decorators import dag, task
import pandas as pd


@dag(
    dag_id="test_dag",
    max_active_tasks=1,
    max_active_runs=1,
    tags=["example"],
)
def test_dag():
    @task
    def pass_xcom() -> pd.DataFrame:
        df = pd.DataFrame(data={"a": [i for i in range(50)]})
        print(df.head())
        return df

    @task
    def recieve_xcom(data: pd.DataFrame):
        print(data.head())

    df = pass_xcom()
    recieve_xcom(df)


test_dag()
