import duckdb
from airflow.sdk import dag, task
from airflow.sdk.bases.hook import BaseHook


@dag(
    dag_id="test_ducklake",
    tags=["test"],
)
def test_dag():
    @task
    def read_some() -> None:
        con = duckdb.connect()
        con.execute("install ducklake;")
        con.execute("install postgres;")

        ducklake_catalog = BaseHook.get_connection("ducklake_catalog")
        ducklake_s3 = BaseHook.get_connection("ducklake_s3")

        con.execute(
            """
                CREATE SECRET (
                    TYPE postgres,
                    HOST ?,
                    PORT ?,
                    DATABASE ?,
                    USER ?,
                    PASSWORD ?
                );
            """,
            [
                ducklake_catalog.host,
                ducklake_catalog.port,
                ducklake_catalog.schema,
                ducklake_catalog.login,
                ducklake_catalog.password,
            ],
        )

        con.execute(
            """
                CREATE OR REPLACE SECRET secret (
                    TYPE s3,
                    ENDPOINT ?,
                    KEY_ID ?,
                    SECRET ?,
                    URL_STYLE 'path',
                    USE_SSL 'false'
                );
            """,
            [
                "seaweedfs-s3.seaweedfs:8333",
                ducklake_s3.login,
                ducklake_s3.password,
            ],
        )

        count = con.execute(
            """
                SELECT count(*)
                FROM 's3://data-raw/backblaze/data_Q3_2025/2025-07-01.csv';
            """
        ).fetchall()
        print(count)

        con.execute(
            """
                ATTACH 'ducklake:postgres:dbname={ducklake_catalog}
                    host={host}' AS my_ducklake (DATA_PATH 's3://ducklake/');
                USE my_ducklake;
            """.format(
                ducklake_catalog=ducklake_catalog.schema,
                host=ducklake_catalog.host,
            )
        )

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
