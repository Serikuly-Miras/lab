from airflow.sdk import dag, task
from custom_operator.ducklake import DuckLakeHook


@dag(
    dag_id="test_ducklake",
    tags=["test"],
)
def test_dag():
    @task
    def read_some() -> None:
        ducklake = DuckLakeHook()
        con = ducklake.get_connection()

        con.execute(
            """
                DROP TABLE IF EXISTS nl_train_stations;
            """
        ).fetchall()

        con.execute(
            """
                CREATE TABLE nl_train_stations AS
                FROM 'https://blobs.duckdb.org/nl_stations.csv';
            """
        ).fetchall()

        count = con.execute(
            """
            SELECT count(*)
            FROM nl_train_stations
            """
        ).fetchall()
        print(count)

    read_some()


test_dag()
