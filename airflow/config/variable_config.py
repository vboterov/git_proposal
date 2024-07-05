{
    "example_case_config": {
        "env_name": "dev",
        "databricks_conn_id": "con-dbw-deid",
        "example_case": {
            "python_file": "dbfs:/repositories/example_case/proposal_example.py",
            "libraries": [],
            "cluster": {
                "num_workers": 0,
                "spark_version": "14.3.x-scala2.12",
                "spark_conf": {
                    "spark.master": "local[*, 4]",
                    "spark.databricks.cluster.profile": "singleNode",
                },
                "azure_attributes": {
                    "first_on_demand": 1,
                    "availability": "ON_DEMAND_AZURE",
                    "spot_bid_max_price": -1,
                },
                "node_type_id": "Standard_D16ads_v5",
                "driver_node_type_id": "Standard_D16ads_v5",
                "custom_tags": {"ResourceClass": "SingleNode"},
                "spark_env_vars": {"PYSPARK_PYTHON": "/databricks/python3/bin/python3"},
                "enable_elastic_disk": true,
                "data_security_mode": "SINGLE_USER",
            },
        },
    }
}
