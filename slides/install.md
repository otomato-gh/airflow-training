# Running Airflow

Let's run Airflow.

Checkout the training repository:

`git clone https://github.com/otomato-gh/airflow-training.git`

Look at the docker-compose definition:

```bash
cd airflow-training
cat airflow/docker-compose.yaml
```

---
## Running Airflow - Distributed Simulation (docker)

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

 - log in with `airflow/airflow`

---

### Running Airflow (standalone)

```bash
cd ~/airflow-training/airflow
./run_standalone.sh
```

Once Airflow is up you will see:
```bash
standalone | Airflow is ready
standalone | Login with username: admin  password: EsF5Xt9HguBXBhWZ
```

Use the credentials shown or `airflow/airflow`