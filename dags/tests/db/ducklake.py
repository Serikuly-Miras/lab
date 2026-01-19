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
                    HOST '{host}',
                    PORT {port},
                    DATABASE {db},
                    USER '{user}',
                    PASSWORD '{password}'
                );
            """.format(
                host=ducklake_catalog.host,
                port=ducklake_catalog.port,
                user=ducklake_catalog.login,
                password=ducklake_catalog.password,
                db=ducklake_catalog.schema,
            )
        )

        con.execute(
            """
                CREATE OR REPLACE SECRET secret (
                    TYPE s3,
                    ENDPOINT '{endpoint}',
                    KEY_ID '{key_id}',
                    SECRET '{secret}',
                    URL_STYLE 'path',
                    USE_SSL 'false'
                );
            """.format(
                endpoint="seaweedfs-s3.seaweedfs:8333",
                key_id=ducklake_s3.login,
                secret=ducklake_s3.password,
            )
        )

        print(
            con.execute(
                """
                SELECT count(*)
                FROM 's3://data-raw/backblaze/data_Q3_2025/2025-07-01.csv';
            """
            ).fetchall()
        )

    read_some()


test_dag()
