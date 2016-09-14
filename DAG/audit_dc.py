#@author: alo-alt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators import SSHExecuteOperator
from airflow.contrib.hooks import SSHHook
from datetime import datetime, timedelta


default_args = {
    'owner': 'alo-alt',
    'depends_on_past': False,
    'start_date': datetime(2016, 7, 6),
    'email': ['devops@evariant.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('audit', default_args=default_args, schedule_interval='45 6 * * *')
ssmaster01 = SSHHook(conn_id='salt01')

# SSH connect
t1 = SSHExecuteOperator(
        task_id='audit_prod',
        ssh_hook = ssmaster01,
	no_host_key_check='True',
        bash_command="sudo salt -t 120 -C '*.internal.prod' state.sls auditing",
        dag=dag)

t2 = SSHExecuteOperator(
        task_id='audit_dev',
        ssh_hook = ssmaster01,
	no_host_key_check='True',
        bash_command="sudo salt -t 120 -C '*.internal.dev' state.sls auditing",
        dag=dag)

t2.set_upstream(t1)

