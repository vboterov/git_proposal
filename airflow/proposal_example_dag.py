import pendulum

from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.providers.databricks.operators.databricks import (
    DatabricksSubmitRunOperator,
)

BASE_NAME = "example_case"
settings_key = f"{BASE_NAME}_config"

start_date = pendulum.datetime(2023, 9, 20, tz="US/Eastern")
settings = Variable.get(settings_key, deserialize_json=True)

env_name = settings["env_name"]
databricks_conn_id = settings["databricks_conn_id"]
example_case_config = settings["example_case"]

args = {
    "owner": "airflow",
    "max_active_tasks": 5,
    "max_active_runs": 1,
}

with DAG(
    dag_id=BASE_NAME,
    default_args=args,
    start_date=start_date,
    schedule_interval=None,
    catchup=False,
    tags=["databricks"],
) as dag:

    start = DummyOperator(
        task_id="start",
    )

    end = DummyOperator(
        task_id="end",
    )

    delivery_fod_deid_packaging = DatabricksSubmitRunOperator(
        task_id=f"example_case_{env_name}",
        databricks_conn_id=databricks_conn_id,
        json={
            "name": "example_case",
            "max_concurrent_runs": 1,
            "tasks": [
                {
                    "task_key": "example_case",
                    "spark_python_task": {
                        "python_file": example_case_config["python_file"],
                        "parameters": [
                            "--job_environment",
                            env_name,
                        ],
                    },
                    "libraries": example_case_config["libraries"],
                    "new_cluster": example_case_config["cluster"],
                }
            ],
            "access_control_list": [
                {
                    "group_name": f"ug-data-engineer-deid-{env_name}",
                    "permission_level": "CAN_MANAGE_RUN",
                }
            ],
        },
        retries=0,
    )

    start >> delivery_fod_deid_packaging >> end
