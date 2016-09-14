#@author: alo-alt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'alo-alt',
    'depends_on_past': False,
    'start_date': datetime(2016, 7, 5),
    # 'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('db_backup', default_args=default_args, schedule_interval='@daily')

backup = """
 exec /home/airflow/scripts/prod_backup.sh
"""
# Backup the DB => /BACKUPS
t1 = BashOperator(
        task_id='run_backup',
        bash_command=backup,
        dag=dag)

t2 = BashOperator(
	task_id='clean_up',
	bash_command='find /BACKUPS/* -mtime +7 -exec rm -f {} \;',
	dag=dag)

t2.set_upstream(t1) 
