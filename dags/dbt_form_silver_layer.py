from cosmos import DbtDag, ProjectConfig, ProfileConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping

profile_config = ProfileConfig(
    profile_name="backblaze",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="dwh",
    ),
)

basic_cosmos_dag = DbtDag(
    project_config=ProjectConfig(
        "/opt/airflow/dags/repo/dags/dbt/backblaze",
    ),
    profile_config=profile_config,
    operator_args={
        "install_deps": True,
        "full_refresh": True,
    },
    schedule_interval="@daily",
    dag_id="backblaze_cosmos_silver_layer",
)
