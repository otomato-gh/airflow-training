# Airflow Scheduler

---
## The Scheduler Workflow

1. Look into Airflow base dag path and parse the python files. Load the available DAG definitions from disk (a.k.a fill the DagBag)

2. Use DAG definitions to identify and/or initialize any *DagRuns* in the metadata db.

3. Check the states of the TaskInstances associated with active DagRuns, resolve any dependencies amongst TaskInstances, identify TaskInstances that need to be executed, and add them to a worker queue, updating the status of newly-queued TaskInstances to "*queued*" in the datbase.
    -  Each available worker pulls a TaskInstance from the queue and starts executing it, updating the database record for the TaskInstance from `queued.` to `running.`
    - Once a TaskInstance is finished running, the associated worker reports back to the queue and updates the status for the TaskInstance in the database (e.g. "finished", "failed",etc.)

4. The scheduler updates the states of all active DagRuns ("running", "failed", "finished") according to the states of all completed associated TaskInstances.

---
### Scheduling Rules:

The scheduler runs the job at the END of each period,starting one `schedule_interval` AFTER the start date. 

So for a `0 19 * * *` schedule (`daily at 19:00 UTC`), the tasks for the `start date 2018-10-27` will start **just after** `2018-10-28 18:59:59.999`

---
### Scheduler Notes:

- The first DAG Run is created based on the minimum `start_date` for the tasks in your DAG.

- The scheduler process creates subsequent `DAG Runs`, based on your DAG’s `schedule_interval`, sequentially.

- If you change the `start_date` of a DAG, you must change the `dag_name` as well.

*credit: * https://medium.com/@dustinstansbury/understanding-apache-airflows-key-concepts-a96efed52b1a

---

### Let's Do Some Scheduling

- As you could've understood from previous slides - the scheduling is dependent on `start_date` and `schedule_interval` properties of a task.

- In our basic DAG the `start_date` was set to today using:

```python
with DAG(
    'first',
    start_date=days_ago(0),
```

- Let's add an interval of each 2 minutes: `*/2 * * * *` :

```python
with DAG(
    'first',
    start_date=days_ago(0),
    schedule_interval='*/2 * * * *',
```

---

### So Many DagRuns

Your scheduler should now be running multiple tasks. Definitely more than one every 2 minutes. Why?

--

Well, basically the scheduler queued all the 2 minute intervals from the start of today. 

So depending on when your day started you should have anywhere between 0 and 720 DagRuns that need to happen.

Having such a long queue is a great opportunity to inspect our Celery executor.

---

### The Celery Executor


- Browse to http://**your_machine_ip**:5555 to see the Flower web interface.

- Explore workers, tasks and brokers.

