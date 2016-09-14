#@author: kris savoy / alex alten

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators import SaltOperator
from datetime import datetime, timedelta
import pprint
import logging

default_args = {
    'owner': 'DevOps',
    'depends_on_past': False,
    'start_date': datetime(2016, 7, 1),
#    'email': ['devops@evariant.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('dc_audit_api', default_args=default_args, schedule_interval='@daily')

#apicmd_prod = """
#  curl -sSk https://ssmaster01.evariant.util:8000/login -c ~/saltapi.cookie -H 'Accept: application/x-yaml' -d username=airflow -d password=3TDDwVskAe3FByq -d eauth=auto && curl -sSk https://ssmaster01.evariant.util:8000 -b ~/saltapi.cookie -H 'Accept: application/x-yaml' -d client=local -d tgt='*.evariant.prod' -d fun=state.sls -d args='auditing' && rm -f saltapi.cookie
#"""

#works!
#def authCheck( resp ):
#	logging.info( pprint.pformat(resp.__dict__) )
#	if ( resp.status_code == 200 ):
#		content = resp.json()
#		
#		logging.info( pprint.pformat(content) )
#			
#		return True
#	else:
#		logging.error( 'Authentication Failure' )
#		return False
#
#auth = SimpleHttpsOperator(
#	task_id='auth',
#	https_conn_id='ssmaster_https',
#	endpoint='login',
#	data={ 'username': 'airflow', 'password': 'test123', 'eauth': 'pam' },
#	response_check=authCheck,
#	dag=dag)

salt = SaltOperator(
	task_id='salt',
	salt_conn_id='ssmaster_https',
	tgt='sstest*',
	fun='test.ping',
	dag=dag
	)

