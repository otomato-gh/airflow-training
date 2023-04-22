# Airflow UI

The Airflow UI makes it easy to:

-  Monitor and troubleshoot your data pipelines.
-  Configure Airflow integrations

---
### DAG View:

List of the DAGs in your environment, and a set of shortcuts to useful pages. You can see exactly how many tasks succeeded, failed, or are currently running at a glance.

<img src="../img/ui/dag_view.png" width="900" height="400">

---
### Tree View:

A tree representation of the DAG that spans across time. If a pipeline is late, you can quickly see where the different steps are and identify the blocking ones.

<img src="../img/ui/tree_view.png" width="900" height="400">

---
### Graph View:

The graph view is perhaps the most comprehensive. Visualize your DAG's dependencies and their current status for a specific run.

<img src="../img/ui/graph_view.png" width="900" height="400">

---

### Gantt Chart:

The Gantt chart lets you analyse task duration and overlap. You can quickly identify bottlenecks and where the bulk of the time is spent for specific DAG runs.

<img src="../img/ui/gantt_charts.png" width="900" height="400">

---
### Task Duration:

The duration of your different tasks over the past N runs. This view lets you find outliers and quickly understand where the time is spent in your DAG over many runs.

<img src="../img/ui/task_duration.png" width="900" height="400">

---

### Landing Time:

The total time spent by a task from the scheduling period including retries. (e.g.) take a `schedule_interval='@daily'` run that finishes at `2016-01-02 03:52:00` landing time is `3:52` (The task scheduled to start at 2016-01-02 00:00:00)

<img src="../img/ui/landing_times.png" width="900" height="400">

---
### Code View:

<img src="../img/ui/code_view.png" width="900" height="400">


---

### Task Instance Context Menu:

From the pages seen above (tree view, graph view, gantt, ...), it is always possible to click on a task instance, and get to this rich context menu that can take you to more detailed metadata, and perform some actions.

<img src="../img/ui/task_instance_view.png" width="900" height="400">


---
### Variables View:

The variables view allows you to manage the key-value pairs of variables used during jobs. 
alue of a variable is considered secret and hidden if the key is one of: 'password', 'secret', 'passwd', 'authorization', 'api\_key', 'apikey', 'access\_token'. It can be configured to show in clear-text.

<img src="../img/ui/variables.png" width="900" height="400">

---
### Browse View:

Browse view allows to drill-down and do bulk operations on Airflow core entities such as `DAG Runs`, `Task Instances`, `Logs`, `Jobs` & `SLA misses`.

<img src="../img/ui/browse.png" width="900" height="400">

---
### Admin View:

The Admin View allows to configure airflow pools, connections, variables, and users.

<img src="../img/ui/admin.png" width="900" height="400">



---

### Airflow Cli Tools:

Airflow has a very rich command line interface that allows for many types of operation on a DAG, starting services, and supporting development and testing.

<img src="../img/ui/airflow_cli.png" width="900" height="400">






