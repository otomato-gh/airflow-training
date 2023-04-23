
# Introduction to Airflow

![w:300, h:300](../img/airflow-svgrepo-com.svg)

---
## What is Airflow?

Airflow is a platform to programmatically author, schedule and monitor workflows.
A workflow is represented as a [DAG (a Directed Acyclic Graph)](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html) and contains individual pieces of work called **Tasks**, arranged with dependencies and data flows taken into account.

![flow](https://airflow.apache.org/docs/apache-airflow/stable/_images/edge_label_example.png)

---

## Airflow History 

Airflow was started in October 2014 by Maxime Beauchemin at Airbnb. It was open-sourced from the very first commit and officially published on the Airbnb Github and announced in June 2015.

The project joined the Apache Software Foundation’s incubation program in March 2016.


---
### Airflow Principles:

- **Dynamic**: Airflow pipelines are configuration as a code (Python), allowing for dynamic pipeline generation. This allows for writing code that instantiates pipelines dynamically.

- **Extensible**: Easily define your own operators, executors and extend the library so that it fits the level of abstraction that suits your environment.

- **Elegant**: Airflow pipelines are lean and explicit. Parameterizing your scripts is built into the core of Airflow using the powerful Jinja templating engine.

- **Scalable**: Airflow has a modular architecture and uses a message queue to orchestrate an arbitrary number of workers. Airflow is ready to scale to infinity.
---

### Scheduling 
In a nutshell, Airflow is like very advanced cron with:

- Retries
- Dependencies between tasks
- SLAs/error notifications
- Metrics: time to complete, number of failures, etc
- Logs
- Visibility

---

## Airflow Architecture

An Airflow installation generally consists of the following components:

- A **scheduler**, which handles both triggering scheduled workflows, and submitting Tasks to the executor to run.

- An **executor**, which handles running tasks. In the default Airflow installation, this runs everything inside the scheduler, but most production-suitable executors actually push task execution out to **workers**.

- A **webserver**, which presents a handy user interface to inspect, trigger and debug the behaviour of DAGs and tasks.

- A folder of DAG files, read by the scheduler and executor (and any workers the executor has)

- A metadata **database**, used by the scheduler, executor and webserver to store state.

---

## Airflow Architecture

<img src="https://airflow.apache.org/docs/apache-airflow/stable/_images/arch-diag-basic.png" height="500" />