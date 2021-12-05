# Airflow Concepts
## DAG:

A DAG (Directed Acyclic Graph) is the core concept of Airflow, collecting Tasks together, organized with dependencies and relationships to say how they should run.

<img style="float: left;" src="https://airflow.apache.org/docs/apache-airflow/stable/_images/basic-dag.png">

Here's a DAG that defines four Tasks - A, B, C, and D - and dictates the order in which they have to run, and which tasks depend on what others. 

It will also say how often to run the DAG - maybe “every 5 minutes starting tomorrow”, or “every day since January 1st, 2020”.

The DAG itself doesn’t care about *what* is happening inside the tasks; it is merely concerned with *how* to execute them - the order to run them in, how many times to retry them, if they have timeouts, and so on.

---

## 3 Ways to Declare a DAG

1) With a context manager:

```python
with DAG("snoop_dag") as dag:
    op = DummyOperator(task_id="task")
```

2) With a constructor, then passing the DAG into Operators:

```python
snoop_dag = DAG("snoop_dag")
op = DummyOperator(task_id="task", dag=snoop_dag)
```

3) With a decorator:

```python
@dag(start_date=days_ago(2))
def generate_dag():
    op = DummyOperator(task_id="task")

snoop_dag = generate_dag()
```
---
## Tasks:

A Task is the basic unit of execution in Airflow. Tasks are arranged into DAGs, and then have upstream and downstream dependencies set between them into order to express the order they should run in.

There are three basic kinds of Task:

 - **Operators** - predefined task templates that you can string together quickly to build most parts of your DAGs.

- **Sensors** -  a special subclass of Operators which are entirely about waiting for an external event to happen.

- A TaskFlow-decorated `@task`, which is a custom Python function packaged up as a Task.

Internally, these are all actually subclasses of Airflow’s BaseOperator, and the concepts of Task and Operator are somewhat interchangeable, but it’s useful to think of them as separate concepts - essentially, Operators and Sensors are templates, and when you call one in a DAG file, you’re making a Task.

---

## Task Relationships

The key part of using Tasks is defining how they relate to each other - their dependencies. 

You declare your Tasks first, and then you declare their dependencies second.

There are two ways of declaring dependencies - using the >> and << (bitshift) operators:

```python
first_task >> second_task >> [third_task, fourth_task]
```
Or the more explicit set_upstream and set_downstream methods:

```python
first_task.set_downstream(second_task)
third_task.set_upstream(second_task)
```

By default, a Task will run when all of its upstream (parent) tasks have succeeded, but there are many ways of modifying this behaviour to add branching, only wait for some upstream tasks, or change behaviour based on where the current run is in history.

---
## Operators:

An Operator is conceptually a template for a predefined Task, that you can just define declaratively inside your DAG:
```python
with DAG("my-dag") as dag:
    ping = SimpleHttpOperator(endpoint="http://example.com/update/")
    email = EmailOperator(to="admin@example.com", subject="Update complete")

    ping >> email
```

Airflow has a very extensive set of operators available, with some built-in to the core or pre-installed providers. Some popular operators from core include:

- BashOperator - executes a bash command
- PythonOperator - calls an arbitrary Python function
- EmailOperator - sends an email

For a list of all core operators, see: [Core Operators and Hooks Reference](https://airflow.apache.org/docs/apache-airflow/stable/operators-and-hooks-ref.html).
---
### Sensors:

Sensors are a special type of Operator that are designed to wait for something to occur. 

It can be time-based, or waiting for a file, or an external event, but all they do is wait until something happens, and then succeed so their downstream tasks can run.

Some popular sensors are:
-  FileSensor: Waits for a file or folder to land in a filesystem.

-  S3KeySensor: Waits for a key to be present in a S3 bucket.

-  SqlSensor: Runs a sql statement repeatedly until a criteria is met.

-  HivePartitionSensor: Waits for a partition to show up in Hive.

-  ExternalTaskSensor: Waits for a different DAG or a task in a different DAG to complete for a specific execution date. 

---

### Task Instances

A task instance represents a specific run of a task and is characterized as the combination of a dag, a task, and a point in time. 

Task instances also have an indicative state, which could be:

 `running`, `success`, `failed`, `skipped`, `up for retry`, etc.

---
### DAG Runs:

A DAG Run is an object representing an instantiation of the DAG in time. DAG runs have a state associated to them (`running`, `failed`, `success`) and informs the scheduler on which set of schedules should be evaluated for task submissions. Without the metadata at the DAG run level, the Airflow scheduler would have much more work to do in order to figure out what tasks should be triggered and come to a crawl.

*Preset Crons:*

| preset     | meaning                                                         | cron        |
| ---------- | --------------------------------------------------------------- | ----------- |
| `None`     | Don't schedule, use for exclusively "externally triggered" DAGs |             |
| `@once`    | Schedule once and only once                                     |             |
| `@hourly`  | Run once an hour at the beginning of the hour                   | `0 * * * *` |
| `@daily`   | Run once a day at midnight                                      | `0 0 * * *` |
| `@weekly`  | Run once a week at midnight on Sunday morning                   | `0 0 * * 0` |
| `@monthly` | Run once a month at midnight of the first day of the month      | `0 0 1 * *` |
| `@yearly`  | Run once a year at midnight of January 1                        | `0 0 1 1 *` |

![airflow_concepts](airflow_concepts.png)
