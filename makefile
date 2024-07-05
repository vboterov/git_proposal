clean:
	make clean-build
	make clean-pyc

clean-build:
	rm -fr dist/
	rm -fr temp/

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '.DS_Store' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

dist:
	mkdir ./dist/

dist-airflow:
	make dist
	mkdir ./dist/airflow
	mkdir ./dist/airflow/config

dist-databricks:
	make dist
	mkdir ./dist/databricks_jobs

lint:
	pipenv run prospector

install:
	pipenv install

install-local:
	pipenv run pre-commit install

# ---------------------------------- #
#               AIRFLOW              #
# ---------------------------------- #

build-airflow-dev:
	cp -r ./airflow/proposal_example_dag.py ./dist/airflow/proposal_example_dev.py
	cp -r ./airflow/config/variable_config.py ./dist/airflow/config/variable_config.py

deploy-airflow-dev:
	cp -r ./dist/airflow/proposal_example_dev.py ./example_azure_storage/dags/example_case/dev/proposal_example.py
	cp -r ./dist/airflow/config/variable_config.py ./example_azure_storage/dags/example_case/dev/config/variable_config.py

build-airflow-uat:
	python3 build.py airflow/proposal_example_dag.py uat
	python3 build.py airflow/config/variable_config.py uat

deploy-airflow-uat:
	cp -r ./dist/airflow/proposal_example_dag.py ./example_azure_storage/dags/example_case/uat/proposal_example.py
	cp -r ./dist/airflow/config/variable_config.py ./example_azure_storage/dags/example_case/uat/config/variable_config.py

build-airflow-prod:
	python3 build.py airflow/proposal_example_dag.py prod
	python3 build.py airflow/config/variable_config.py prod

deploy-airflow-prod:
	cp -r ./dist/airflow/proposal_example_dag.py ./example_azure_storage/dags/example_case/prod/proposal_example.py
	cp -r ./dist/airflow/config/variable_config.py ./example_azure_storage/dags/example_case/prod/config/variable_config.py

full-airflow-dev:
	make clean
	make dist-airflow
	make build-airflow-dev
	make deploy-airflow-dev

full-airflow-uat:
	make clean
	make dist-airflow
	make build-airflow-uat
	make deploy-airflow-uat

full-airflow-prod:
	make clean
	make dist-airflow
	make build-airflow-prod
	make deploy-airflow-prod

# ---------------------------------- #
#             DATABRICKS             #
# ---------------------------------- #

build-databricks-job:
	cp databricks_jobs/proposal_example.py  dist/databricks_jobs/proposal_example.py

deploy-databricks-job:
	cp dist/databricks_jobs/proposal_example.py ./example_azure_storage/code/example_case/proposal_example.py

full-databricks:
	make clean
	make dist-databricks
	make build-databricks-job
	make deploy-databricks-job
