from datetime import datetime
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.trino.hooks.trino import TrinoHook

TRINO_CONN_ID = "trino"
CATALOG = "iceberg"
SCHEMAS = ["bronze", "silver", "gold"]


def _discover_tables():
    schema_list = ", ".join(f"'{s}'" for s in SCHEMAS)
    hook = TrinoHook(trino_conn_id=TRINO_CONN_ID)
    rows = hook.get_records(
        f"""
        SELECT table_schema, table_name
        FROM {CATALOG}.information_schema.tables
        WHERE table_schema IN ({schema_list})
          AND table_type = 'BASE TABLE'
        ORDER BY table_schema, table_name
        """
    )
    return [(row[0], row[1]) for row in rows]


TABLES = _discover_tables()


with DAG(
    dag_id="iceberg_maintenance",
    schedule="0 11 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["iceberg", "maintenance"],
) as dag:
    for schema, table in TABLES:
        qualified = f"{CATALOG}.{schema}.{table}"

        # 1. Expire snapshots older than 7 days
        expire = SQLExecuteQueryOperator(
            task_id=f"expire_snapshots__{schema}__{table}",
            conn_id=TRINO_CONN_ID,
            sql=f"""
                ALTER TABLE {qualified}
                EXECUTE expire_snapshots(retention_threshold => '7d')
            """,
        )

        # 2. Remove orphan files
        orphan = SQLExecuteQueryOperator(
            task_id=f"remove_orphans__{schema}__{table}",
            conn_id=TRINO_CONN_ID,
            sql=f"""
                ALTER TABLE {qualified}
                EXECUTE remove_orphan_files(retention_threshold => '7d')
            """,
        )

        # 3. Compact small files
        compact = SQLExecuteQueryOperator(
            task_id=f"compact_files__{schema}__{table}",
            conn_id=TRINO_CONN_ID,
            sql=f"""
                ALTER TABLE {qualified}
                EXECUTE optimize(file_size_threshold => '128MB')
            """,
        )

        # 4. Optimize manifests
        manifests = SQLExecuteQueryOperator(
            task_id=f"optimize_manifests__{schema}__{table}",
            conn_id=TRINO_CONN_ID,
            sql=f"""
                ALTER TABLE {qualified}
                EXECUTE optimize_manifests
            """,
        )

        compact >> expire >> orphan >> manifests
