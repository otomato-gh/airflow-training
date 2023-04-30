# Airflow Operators:

While DAGs describe how to run a workflow, Operators determine what gets done.

An operator describes a single task in a workflow. Operators are usually (but not always) atomic, meaning they can stand on their own and don’t need to share resources with any other operators. The DAG will make sure that operators run in the certain correct order; other than those dependencies, operators generally run independently. They may run on two completely different machines.

There are over 100 operators shipped with Airflow. Airflow operators can be broadly categorized into three categories.

---

### Action Operators:

The action operators perform some action such as executing a Python function or submitting a Spark Job.

 (e.g.) BashOperator, PythonOperator, DockerOperator, OracleOperator

---
### Sensor Operators:

The Sensor operators trigger downstream tasks in the dependency graph when a specific criterion is met, for example checking for a particular file becoming available on S3 before using it downstream. Sensors are a dominant feature of Airflow allowing us to create complex workflows and efficiently manage their preconditions.

(e.g.) S3KeySensors, HivePartitionSensor, ExternalTaskSensor, TimeSensor

---

### Transfer Operators:

Transfer Operators move data between systems such as from Hive to Mysql or from S3 to Hive.

(e.g.) GenericTransfer,MsSqlToHiveTransfer, RedshiftToS3Transfer


---
### Operator Properties:

| Property                    | Desc                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Default                |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| dag                         | a reference to the dag the task is attached to                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Mandatory param        |
| task_id                     | a unique, meaningful id for the task                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Mandatory param        |
| trigger_rule                       | defines the rule by which dependencies are applied for the task to get triggered                                    | Mandatory param        |                                                                                                                                                                                                                                                                                                             
---
### Bash Operators:

Execute a Bash script, command or set of commands. (e.g.) Bash Operator to clean /tmp files periodically. 

```python
clean_tmp_dir = BashOperator(
    task_id='clean_tmp_dir',
    bash_command='find /tmp -mtime +2 -type f -exec rm -rf {} \;',
    dag='cleaner_dag'
)
```
---
### Python Operators:

Executes a Python callable method.

```python
def my_sleeping_function(random_base):
    """This is a function that will run within the DAG execution"""
    time.sleep(random_base)
    
for i in range(10): # loop in to create dynamic operators.
    task = PythonOperator(
        task_id='sleep_for_' + str(i), # task id should be unique
        python_callable=my_sleeping_function, # python callable method
        op_kwargs={'random_base': float(i) / 10}, # pass the method argument here
        dag=dag)
```
---
### Branch Operators:

Allows a workflow to "branch" or follow a single path following the execution of this task.

It derives the PythonOperator and expects a Python function that returns the task\_id to follow. The task\_id returned should point to a task directly downstream from {self}. All other `branches` or directly downstream tasks are marked with a state of `skipped` so that these paths can't move forward. The \`\`skipped\`\` states are propagated downstream to allow for the DAG state to fill up and the DAG run's state to be inferred. Note that using tasks with `depends_on_past=True` downstream from `BranchPythonOperator` is logically unsound as `skipped` status will invariably block tasks that depend on their past successes.`skipped` state propagates where all directly upstream tasks are`skipped`.

```python
branching = BranchPythonOperator(
    task_id='branching',
    python_callable=lambda: random.choice(options),
    dag=dag)
```

---

### Branch Operators 

.exercise[
- Execute the `example_branch_operator` DAG

- Check the execution graph

- Notice how the `join` task got skipped

- Why?

]

---


### A Side-note: trigger_rules

All operators define a `trigger_rule` property with the default value set to `all_success`

All possible values: `{ all_success | all_failed | all_done | one_success | one_failed | dummy}`

`trigger_rule` helps us when using the BranchPythonOperator


---

### Fixing the trigger_rule

.exercise[
Change the file `~/airflow-training/dags/airflow-operators/branch.py` :

```python
join = DummyOperator(
    task_id='join',
    trigger_rule='one_success',
    dag=dag
)
```

Rerun the DAG and make sure `join` is now executed as expected.

]

---

### Short Circuit Operators:

Allows a workflow to continue only if a condition is met. Otherwise, the workflow `short-circuits` and downstream tasks are skipped.  

The ShortCircuitOperator is derived from the PythonOperator. It evaluates a condition and short-circuits the workflow if the condition is False. Any downstream tasks are marked `skipped`. If the condition is `True`, downstream tasks proceed as normal.  

The condition is determined by the result of `python_callable`.

```python
cond_true = ShortCircuitOperator(
    task_id='condition_is_True', python_callable=lambda: True, dag=dag)

cond_false = ShortCircuitOperator(
    task_id='condition_is_False', python_callable=lambda: False, dag=dag)
```

---

### Exercise - Short Circuit Operator

- Based on the example of `airflow_operators/short_circuit.py`

- Please create your own DAG with a python function that randomly returns `true | false`

- Create a ShortCircuitOperator that uses that function and either continues the execution to next task or stops the workflow.

- Downstream task:
```python
BashOperator(
        task_id='show_weather',
        bash_command='curl wttr.in/israel',
    )
```
---

### Running individual tasks:

```bash
airflow test <dag_id> <task_id> <execution date> (or)
airflow test -tp {'param1': 'my_param'} <dag_id> <task_id> <execution_date>
```

---

### Writing Custom Operators:

In order to write a custom operator we need to :
- extend the `BaseOperator` class
- `override` the constructor and the `execute` method.

(e.g.) A custom Airflow operator to `zip` all the files in a given directory (see next slide)

---
### Zip Operator
```python
class ZipOperator(BaseOperator):
    
    template_fields = ('path_to_file_to_zip', 'path_to_save_zip')
    template_ext = []

    @apply_defaults
    def __init__(
            self,
            path_to_file_to_zip,
            path_to_save_zip,
            *args, **kwargs):
        self.path_to_file_to_zip = path_to_file_to_zip
        self.path_to_save_zip = path_to_save_zip

    def execute(self, context):
        logging.info("Executing ZipOperator.execute(context)")
```
Full code [here](https://gist.github.com/antweiss/28508b5f37a32ad7474d80b8527b7837)


