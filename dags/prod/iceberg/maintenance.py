from datetime import datetime
from airflow.decorators import dag, task
from airflow.providers.trino.hooks.trino import TrinoHook

TRINO_CONN_ID = "trino"
CATALOG = "iceberg"
SCHEMAS = ["bronze", "silver", "gold"]


@dag(
    dag_id="iceberg_maintenance",
    schedule="0 11 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["iceberg", "maintenance"],
)
def iceberg_maintenance():

    @task
    def discover_tables() -> list[dict]:
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
        return [{"schema": row[0], "table": row[1]} for row in rows]

    @task
    def maintain_table(table_info: dict) -> None:
        qualified = f"{CATALOG}.{table_info['schema']}.{table_info['table']}"
        hook = TrinoHook(trino_conn_id=TRINO_CONN_ID)

        # 1. Compact small files
        hook.run(
            f"ALTER TABLE {qualified} EXECUTE optimize(file_size_threshold => '128MB')"
        )

        # 2. Expire snapshots older than 7 days
        hook.run(
            f"ALTER TABLE {qualified} EXECUTE expire_snapshots(retention_threshold => '7d')"
        )

        # 3. Remove orphan files
        hook.run(
            f"ALTER TABLE {qualified} EXECUTE remove_orphan_files(retention_threshold => '7d')"
        )

        # 4. Optimize manifests
        hook.run(f"ALTER TABLE {qualified} EXECUTE optimize_manifests")

    maintain_table.expand(table_info=discover_tables())


iceberg_maintenance()
