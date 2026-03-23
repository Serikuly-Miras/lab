from cosmos import DbtDag, ProjectConfig, ProfileConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping

profile_config = ProfileConfig(
    profile_name="backblaze",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="dwh",
        profile_args={"schema": "silver"},
    ),
)

basic_cosmos_dag = DbtDag(
    project_config=ProjectConfig(
        "/opt/airflow/dags/repo/dags/dbt/backblaze",
        install_dbt_deps=True,
    ),
    profile_config=profile_config,
    operator_args={
        "install_deps": True,
        "full_refresh": True,
    },
    schedule="@once",
    dag_id="backblaze_cosmos_silver_layer",
)
