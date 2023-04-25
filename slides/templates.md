
# Macros & Templates

Airflow leverages the power of Jinja Templating, and this can be a powerful tool to use in combination with macros. 

Macros are a way to expose objects to your templates. 
Macros reside in the `macros` namespace in your templates.

Airflow built-in macros: 

https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html#macros

Airflow built-in templates variables: 

https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html#variables

---

### The Basics of Templating

Let's see how to use built-in variables and templates in our tasks.

- Add the content of this [gist](https://gist.github.com/antweiss/07eb87d3d86cb448d319af22f22dde3d)  in `myfirstdag.py` in ~/airflow-training/airflow/dags:

- Execute your DAG from the UI

- Check the task executions and their logs


---

### Templating with PythonOperator

The PythonOperator is an exception to the templating. It accepts a python_callable argument in which the runtime context may be applied, rather than the arguments that can be templated with the runtime context.

- Add a new file `mynewdag.py` in ~/airflow-training/airflow/dags:
- Use the code from this [gist](https://gist.github.com/antweiss/d2740c248b0ddcdefc535303eb83494b)

- Execute your DAG from the UI

- Check the task executions and their logs

---

### Templating with PythonOperator
.exercise[
- Change your sleeping function to 
```python
def my_sleeping_function(random_base, ds):
    """This is a function that will run within the DAG execution"""
    print("Starting at ", ds)
    time.sleep(random_base)
```
- And add this is in PythonOperator envocation:
```python
   op_kwargs={'random_base': i, "ds": "{{ ds }}" },
```
]

---

### Templating with PythonOperator


- Execute your DAG from the UI

- Check the task executions and their logs

---

### Joining the Tasks

.exercise[
- Add the following task in `mynewdag.py`:
```python
join = DummyOperator(
  task_id = "join"
)
```
- Now add all your generated templated sleep commands to a list and make `join` depend on that list:
```python
  [sleeping_list] >> join
```
- Rerun and check results 
]

---

### Using Our Own Variables

In addition to built-in Airflow variables we can define instance-wide variables.

- In the UI go to Admin -> Variables

- Define a variable "COMPANY" with value "Otomato"

- Now add a BashOperator task in `mynewdag.py` to echo that variable by using the `{{ var.value.get('COMPANY') }}` macro
```python
  bash_command = "echo {{ var.value.get('COMPANY') }} "
```

---

##### Custom airflow macros:

Step 1: define the custom macro

```python
CUSTOM_MACROS = {
  'echo': lambda id: 'echo ' + id
}
```

Step 2: configure the macro in the airflow dag definition

```python
dag = DAG(
    dag_id='custom_macro_dag', default_args=args,
    schedule_interval='0 0 * * *',
    dagrun_timeout=timedelta(minutes=60),
    user_defined_macros=CUSTOM_MACROS # user defined macros added to the dag context
)
```

---

### Custom macros

Step 3: Access using jinja template variables

```python
CMD ='{{echo("joe")}}'
task = BashOperator(
        task_id='runme',
        bash_command=CMD,
        dag=dag)
```

---

### Exercise

- Create a new dag with a custom macro definition based on the previous slides.

- Execute the dag to make sure all works correctly.