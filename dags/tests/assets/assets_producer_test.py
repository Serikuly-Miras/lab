from airflow.sdk import Asset, dag, task


@dag(
    tags=["test"],
)
def assets_producer_test():
    @task(outlets=[Asset("test")])
    def my_producer_task():
        pass

    my_producer_task()


assets_producer_test()
