from pathlib import Path

from cosmos import DbtDag, ProjectConfig, ProfileConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping

DBT_ROOT_PATH = Path(__file__).parent.parent.parent / "dbt"  # todo : fix

profile_config = ProfileConfig(
    profile_name="backblaze",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="dwh",
    ),
)

basic_cosmos_dag = DbtDag(
    project_config=ProjectConfig(
        DBT_ROOT_PATH / "backblaze",
    ),
    profile_config=profile_config,
    operator_args={
        "install_deps": True,
        "full_refresh": True,
    },
    schedule_interval="@daily",
    dag_id="backblaze_cosmos_silver_layer",
)
