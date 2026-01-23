import logging
from typing import Optional

import duckdb
from airflow.sdk.bases.hook import BaseHook


class DuckLakeHook(BaseHook):
    """Custom hook for working with DuckLake using DuckDB."""

    def __init__(
        self,
        ducklake_catalog_conn_id: str = "ducklake_catalog",
        ducklake_s3_conn_id: str = "ducklake_s3",
    ):
        super().__init__()
        self.ducklake_catalog_conn_id = ducklake_catalog_conn_id
        self.ducklake_s3_conn_id = ducklake_s3_conn_id
        self.log = logging.getLogger(__name__)
        self._connection: Optional[duckdb.DuckDBPyConnection] = None

    def get_connection(self) -> duckdb.DuckDBPyConnection:
        """Get or create DuckDB connection with DuckLake setup."""
        if self._connection is None:
            self._connection = self._create_connection()
        return self._connection

    def _create_connection(self) -> duckdb.DuckDBPyConnection:
        """Create and configure DuckDB connection with DuckLake."""
        con = duckdb.connect()

        # Install required extensions
        con.execute("INSTALL ducklake;")
        con.execute("INSTALL postgres;")

        # Setup secrets
        self._setup_secrets(con)

        # Attach DuckLake catalog
        self._attach_ducklake(con)

        return con

    def _setup_secrets(self, con: duckdb.DuckDBPyConnection) -> None:
        """Setup secrets for DuckLake catalog and S3 storage."""
        ducklake_catalog = BaseHook.get_connection(self.ducklake_catalog_conn_id)  # noqa
        ducklake_s3 = BaseHook.get_connection(self.ducklake_s3_conn_id)

        con.execute(
            """
            CREATE SECRET ducklake_catalog_secret (
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
            CREATE OR REPLACE SECRET ducklake_s3_secret (
                TYPE s3,
                ENDPOINT ?,
                KEY_ID ?,
                SECRET ?,
                URL_STYLE 'path',
                USE_SSL 'false'
            );
            """,
            [
                self.s3_endpoint,
                ducklake_s3.login,
                ducklake_s3.password,
            ],
        )

    def _attach_ducklake(self, con: duckdb.DuckDBPyConnection) -> None:
        """Attach DuckLake catalog to the connection."""
        ducklake_catalog = BaseHook.get_connection(self.ducklake_catalog_conn_id)  # noqa

        con.execute(
            """
            ATTACH 'ducklake:postgres:dbname={db} host={host} port={port}'
            AS ducklake (DATA_PATH ?);
            USE ducklake;
            """.format(
                db=ducklake_catalog.schema,
                host=ducklake_catalog.host,
                port=ducklake_catalog.port or 5432,
            ),
            [self.data_path],
        )
