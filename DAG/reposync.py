#@author: alo-alt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators import SSHExecuteOperator
from airflow.contrib.hooks import SSHHook
from datetime import datetime, timedelta


default_args = {
    'owner': 'alo-alt',
    'depends_on_past': False,
    'start_date': datetime(2016, 7, 26),
    'email': ['add@email.here'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('reposync', default_args=default_args, schedule_interval='0 18 * * 7')
repo = SSHHook(conn_id='repo')

# Sync OS repos
t1 = SSHExecuteOperator(
        task_id='centos7',
        ssh_hook = repo,
        bash_command="/usr/bin/rsync -avz --delete --exclude='repo*' rsync://mirror.cisp.com/CentOS/7/os/x86_64/ /var/www/html/repos/centos/7/os/x86_64/",
        dag=dag)

t2 = SSHExecuteOperator(
        task_id='centos6',
        ssh_hook = repo,
        bash_command="/usr/bin/rsync -avz --delete --exclude='repo*' rsync://mirror.cisp.com/CentOS/6/os/x86_64/ /var/www/html/repos/centos/6/os/x86_64/",
        dag=dag)

t3 = SSHExecuteOperator(
        task_id='updates7',
        ssh_hook = repo,
        bash_command="/usr/bin/rsync -avz --delete --exclude='repo*' rsync://mirror.cisp.com/CentOS/7/updates/x86_64/ /var/www/html/repos/centos/7/updates/x86_64/",
        dag=dag)

t4 = SSHExecuteOperator(
        task_id='updates6',
        ssh_hook = repo,
        bash_command="/usr/bin/rsync -avz --delete --exclude='repo*' rsync://mirror.cisp.com/CentOS/6/updates/x86_64/ /var/www/html/repos/centos/6/updates/x86_64/",
        dag=dag)

t5 = SSHExecuteOperator(
        task_id='epel7',
        ssh_hook = repo,
        bash_command="/usr/bin/rsync -avz --delete --exclude='repo*' --exclude='debug' rsync://mirrors.rit.edu/epel/7/x86_64/ /var/www/html/repos/epel/7/x86_64/",
        dag=dag)

t6 = SSHExecuteOperator(
        task_id='epel6',
        ssh_hook = repo,
        bash_command="/usr/bin/rsync -avz --delete --exclude='repo*' --exclude='debug' rsync://mirrors.rit.edu/epel/6/x86_64/ /var/www/html/repos/epel/6/x86_64/",
        dag=dag)

# Update OS repo files

t7 = SSHExecuteOperator(
        task_id='repo_os7',
        ssh_hook = repo,
        bash_command="/usr/bin/createrepo --update /var/www/html/repos/centos/7/os/x86_64/",
        dag=dag)

t8 = SSHExecuteOperator(
        task_id='repo_os6',
        ssh_hook = repo,
        bash_command="/usr/bin/createrepo --update /var/www/html/repos/centos/6/os/x86_64/",
        dag=dag)

t9 = SSHExecuteOperator(
        task_id='repo_update7',
        ssh_hook = repo,
        bash_command="/usr/bin/createrepo --update /var/www/html/repos/centos/7/updates/x86_64/",
        dag=dag)

t10 = SSHExecuteOperator(
        task_id='repo_update6',
        ssh_hook = repo,
        bash_command="/usr/bin/createrepo --update /var/www/html/repos/centos/6/updates/x86_64/",
        dag=dag)

t11 = SSHExecuteOperator(
        task_id='repo_epel7',
        ssh_hook = repo,
        bash_command="/usr/bin/createrepo --update /var/www/html/repos/epel/7/x86_64/",
        dag=dag)

t12 = SSHExecuteOperator(
        task_id='repo_epel6',
        ssh_hook = repo,
        bash_command="/usr/bin/createrepo --update /var/www/html/repos/epel/6/x86_64/",
        dag=dag)

# Salt repo sync

t13 = SSHExecuteOperator(
        task_id='salt_redhat',
        ssh_hook = repo,
        bash_command="/usr/bin/rsync -avz --exclude='repo*' rsync://repo.saltstack.com/saltstack_pkgrepo_rhel/ /var/www/html/repos/saltstack/redhat/",
        dag=dag)

t14 = SSHExecuteOperator(
        task_id='repo_salt_redhat6.7',
        ssh_hook = repo,
        bash_command="/usr/bin/createrepo --update /var/www/html/repos/saltstack/redhat/redhat/6.7/x86_64/2015.8/",
        dag=dag)

t15 = SSHExecuteOperator(
        task_id='repo_salt_redhat6.8',
        ssh_hook = repo,
        bash_command="/usr/bin/createrepo --update /var/www/html/repos/saltstack/redhat/redhat/6.8/x86_64/2015.8/",
        dag=dag)

t16 = SSHExecuteOperator(
        task_id='repo_salt_redhat7',
        ssh_hook = repo,
        bash_command="/usr/bin/createrepo --update /var/www/html/repos/saltstack/redhat/redhat/7/x86_64/2015.8/",
        dag=dag)

t17 = SSHExecuteOperator(
        task_id='salt_windows',
        ssh_hook = repo,
        bash_command="/usr/bin/rsync -avz --exclude='repo*' rsync://repo.saltstack.com/saltstack_pkgrepo_windows/ /var/www/html/repos/saltstack/windows/",
        dag=dag)


t7.set_upstream(t6)
t8.set_upstream(t7)
t9.set_upstream(t8)
t10.set_upstream(t9)
t11.set_upstream(t10)
t12.set_upstream(t11)
t13.set_upstream(t6)
t14.set_upstream(t13)
t15.set_upstream(t14)
t16.set_upstream(t15)
t17.set_upstream(t13)
