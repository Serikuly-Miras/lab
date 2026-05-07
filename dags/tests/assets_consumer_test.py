from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import Asset, dag


@dag(
    schedule=[Asset("test")],
    tags=["test"],
)
def assets_consumer_test():
    EmptyOperator(task_id="empty_task")


assets_consumer_test()
