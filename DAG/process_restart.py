#@author: alo-alt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators import SSHExecuteOperator
from airflow.contrib.hooks import SSHHook
from datetime import datetime, timedelta


default_args = {
    'owner': 'alo-alt',
    'depends_on_past': False,
    'start_date': datetime(2016, 7, 9),
    'email': ['instert@here, 2nd@works.too'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('restart_process', default_args=default_args, schedule_interval='0 12 * * 6')
listener01 = SSHHook(conn_id='server01')
listener02 = SSHHook(conn_id='server02')

# SSH connect
t1 = SSHExecuteOperator(
        task_id='restart_nginx',
        ssh_hook = server01,
        bash_command="sudo service nginx restart",
        dag=dag)

t2 = SSHExecuteOperator(
        task_id='restart_postfix',
        ssh_hook = server02,
        bash_command="sudo service postfix restart",
        dag=dag)
t3 = SSHExecuteOperator(
        task_id='check_nginx',
	ssh_hook = server01,
        bash_command="sudo service nginx status",
        dag=dag)

t4 = SSHExecuteOperator(
        task_id='check_postfix',
        ssh_hook = server02,
        bash_command="sudo service postfix status",
        dag=dag)

t3.set_upstream(t1)
t2.set_upstream(t3)
t4.set_upstream(t2)

