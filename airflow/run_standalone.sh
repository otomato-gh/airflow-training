#! /bin/bash

sudo apt update
sudo apt install -y python3-pip

export AIRFLOW_HOME=~/airflow-training/airflow

# Install Airflow using the constraints file
AIRFLOW_VERSION=2.5.3
PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.7
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.5.3/constraints-3.7.txt
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
pip install apache-airflow-providers-postgres==5.4.0

export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__CORE__DAGS_FOLDER=~/airflow-training/dags
export AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL=60
export AIRFLOW__CORE__EXPOSE_CONFIG=True
export PATH=${PATH}:~/.local/bin
# The Standalone command will initialise the database, make a user,
# and start all components for you.
airflow standalone &
airflow users  create --role Admin --username airflow --email airflow@otomato.io --firstname airflow --lastname airflow --password airflow
