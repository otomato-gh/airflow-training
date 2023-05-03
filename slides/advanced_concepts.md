# Advanced Airflow Concepts
---
### Airflow Hooks:

Hooks are an interface to interact with external systems. Hooks handle the connection and interaction to specific instances of these systems, and expose consistent methods to interact with them.

Hooks abstract away a lot of boilerplate code and serve as a building block for Airflow operators. Airflow operators, then, do the actual work of fetching or transforming data

Some of the built-in hooks are,

- HiveHook
- mysql
- mssql
- oracle
- http
- Slack
---

#### Custom Hook:

extend `BaseHook` class and override `get_conn`, `get_records`, `run` methods as needed

---

### Connections:

Connections store information about external data sources and credentials to access them. 

The idea here is that scripts use references to database instances (conn_id) instead of hard-coding hostname, logins and passwords when using operators or hooks.

```python
create_pet_table = PostgresOperator(
    task_id="create_pet_table",
    postgres_conn_id="postgres_default",
    sql="sql/pet_schema.sql",
)
```

---

#### Airflow connections via Airflow UI

##### List all the connections:

<img src="../img/connection_create.png" width="800" height="350">
---

##### Create a new connection:

<img src="../img/48.png" width="900" height="400">

---

#### Airflow connections via environment variable:

Airflow will consider any environment variable with the prefix `AIRFLOW_CONN`.

E.g:  to set `S3_DEFAULT` connection, you can set the environment variable `AIRFLOW_CONN_S3_DEFAULT`

Example (for a db connection):
```bash
export AIRFLOW_CONN_MY_PROD_DATABASE='{
    "conn_type": "my-conn-type",
    "login": "my-login",
    "password": "my-password",
    "host": "my-host",
    "port": 1234,
    "schema": "my-schema",
}'
```
---

### Exercise - Connections and Hooks

- Let's create a PostgreSQL DB

```bash
sudo docker run -v ~/airflow-training:/data --name my-postgres -e POSTGRES_PASSWORD=otomato \
 -d  -p 5432:5432 postgres

 # And create a table:
sudo docker exec -it some-postgres psql -h localhost -U postgres

 # And populate it
CREATE TABLE customer(
    id serial,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(50)
);

exit
```
---

### Exercise - Connections and Hooks

- Now let's create a connection:
- In UI go to Admin -> Connections
- Find the `postgres_default`
- Fill it out:
    - "conn_type": "Postgres"
    - "login": "postgres"
    - "password": "otomato"
    - "host": "localhost"
    - "port": 5432
    - "schema": "postgres"
- Test the connection by clicking on `Test`

---

### Exercise - Connections and Hooks

- Create a CSV file `~/airflow-training/customers.csv` using the format below:
```csv
serial,first_name,last_name,email
1,john,michael,john@gmail.com
2,mary,cooper,mcooper@gmail.com
3,sheldon,cooper,scooper@gmail.com
4,john,michael,john@gmail.com
5,mary,cooper,mcooper@gmail.com
6,sheldon,cooper,scooper@gmail.com
```

---

### Populate the DB table from the file
```bash
sudo docker exec -it some-postgres psql -h localhost -U postgres

COPY customer FROM '/data/customers.csv' DELIMITER ',' CSV HEADER;

exit
```

---

### Run the DAG

- Find the DAG named `pg_extract`

- Inspect the code

- Trigger DAG

- Check file `~/airflow-training/customers-ex.csv`

---

### Variables:

Variables are a generic way to store and retrieve arbitrary content or settings as a simple key-value store within Airflow.It is useful to set environment variable to pass across the pipeline.

<img src="../img/variables.png" width="800" height="300">

---

### Setting variables in code

Apart from UI, we can set environment variable programmatically as well, 

```python
from airflow.models import Variable
Variable.set("foo","value")
foo = Variable.get("foo")
## set json as a value
Variable.set("bar",'{ "name":"John", "age":30, "city":"New York"}') 
## deserialize json value
bar = Variable.get("bar", deserialize_json=True) 
```

---
### XCom:

XComs, or short for "cross-communication" are stores of key, value, and timestamps meant to communicate between tasks. 

XComs are stored in Airflow's metadata database with an associated `execution_date`, `TaskInstance`, and `DagRun`.

XComs can be “pushed” (sent) or “pulled” (received). 

When a task pushes an XCom, it makes it generally available to other tasks. Tasks can push XComs at any time by calling the`xcom_push()`method.

---

### Xcom Example

XComs are explicitly "pushed" and "pulled" to/from their storage using the `xcom_push` and `xcom_pull` methods on Task Instances. Many operators will auto-push their results into an XCom key called `return_value` if the `do_xcom_push` argument is set to `True` (as it is by default), and `@task` functions do this as well.

`xcom_pull` defaults to using this key if no key is passed to it, meaning it's possible to write code like this:

```python
 # Pulls the return_value XCOM from "pushing_task"
value = task_instance.xcom_pull(task_ids='pushing_task')
```