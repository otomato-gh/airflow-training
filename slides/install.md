# Running Airflow

Let's run Airflow.

Checkout the training repository:

`git clone https://github.com/otomato-gh/airflow-training.git`

Look at the docker-compose definition:

`cat airflow/docker-compose.yaml`

---
## Running Airflow

```bash
cd ~/airflow-training/airflow
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker-compose up -d
```
Check the status of webserver:
```bash
docker-compose ps airflow-webserver
```

When your `airflow_airflow-webserver_1` shows:
```
State   
-------------
Up (healthy)
```

 - access the web server http://your.machine.ip:8080

