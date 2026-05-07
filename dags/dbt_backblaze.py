from cosmos import DbtDag, ProjectConfig, ProfileConfig
from cosmos.profiles.starrocks.user_pass import StarrocksUserPasswordProfileMapping


class StarrocksNoPasswordProfileMapping(StarrocksUserPasswordProfileMapping):
    required_fields = [
        "host",
        "username",
        "port",
        "schema",
    ]

    secret_fields = []

    @property
    def profile(self):
        profile = {
            **self.mapped_params,
            **self.profile_args,
        }
        return self.filter_null(profile)


profile_config = ProfileConfig(
    profile_name="backblaze",
    target_name="dev",
    profile_mapping=StarrocksNoPasswordProfileMapping(
        conn_id="starrocks",
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
    dag_id="backblaze_cosmos_silver_layer",
)
