# SmartAI

Smart way of mapping candidates to the job requirements.

## Prerequisites

* Make sure you have update all system `apt` packages (Ubuntu)
  
  `sudo apt-get update && sudo apt-get upgrade`

* Requires `Python >= 3.6` and `pip`

    * Check installation version: `python --version`
 
    * Install (Ubuntu): `sudo apt-get update && sudo apt-get install python3.6`

    * Install (Windows): https://docs.python.org/3/using/windows.html#installation-steps

* Requires `virtualenv`
    
    * Install: `pip install virtualenv`

* Requires `virtualenvwrapper` on windows
    
    * Install (Windows): `pip install virtualenvwrapper-win`

## Setup Virtual Environment & Other Configurations

#### Create Virtual Environment

> virtualenv -p python3 venv


#### Activate Virtualenv

[Ubuntu]
> source venv/bin/activate

[Windows]
> venv\Scripts\activate.bat


#### Deactivate Virtualenv

> deactivate


#### Install Requirements

> `pip install -r requirements.txt`

#### Run server locally
> python manage.py runserver

#### You can access home page here
> 127.0.0.1:8000

#### To get all available commands:
> python manage.py --help

#### Check for Migrations
> python manage.py makemigrations

#### Migrate Tables
> python manage.py migrate

## Install Redis

Our task scheduling mechanism (Celery) uses `brokers` to pass message between 
our django project and the workers for our tasks. We will be using redis as a 
broker for our project. More information on celery can be found on 
https://docs.celeryproject.org/en/stable/ and on redis can be found on 
https://redis.io/. Please install redis on the machine using the following 
instructions depending on your operating system. 


#### Ubuntu

> wget http://download.redis.io/redis-stable.tar.gz

> tar xvzf redis-stable.tar.gz

> cd redis-stable

> make

Copy both the Redis server and the Redis CLI into the PATH variable location
of your machine. You can use the following commands:

> sudo cp src/redis-server /usr/local/bin/

> sudo cp src/redis-cli /usr/local/bin/

Alternatively, you can simply use the `sudo make install` command to do the job. 

#### Windows

* Visit the Redis Github repository at https://github.com/MicrosoftArchive/redis/

* Scroll down to the “Redis on Windows” section and click on the release page link.

* Find the latest version and download the .msi file.

* Run the .msi file and follow the Setup Wizard instructions. make sure to check the 
  “Add the Redis installation folder to the Path environment variable” checkbox.
  
* After the installation is completed, you might want to check the PATH variable on 
  your machine for the location of your Redis installation. If it does not contain one, 
  you need to add it manually. The location generally is `C:\Program Files\Redis\` but 
  do check once.
  
#### Testing the Redis Installation

Use the following command to fire up your redis server:
> redis-server

If the installation is fine, you will be able to see a message that the server has started.

You can test that Redis is working properly by executing the following command from your terminal:

> redis-cli ping 

If the redis replies with `PONG`, it means that that things are working fine. 

## ODBC Driver Installation

We will be using `pyodbc` driver to connect to the database. For this, we need to install the ODBC 
drivers on our machine. Use the following instructions for installation depending on your operating 
system.

#### Ubuntu

```
sudo su
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

#Download appropriate package for the OS version
#Choose only ONE of the following, corresponding to your OS version

#Ubuntu 16.04
curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

#Ubuntu 18.04
curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

#Ubuntu 19.10
curl https://packages.microsoft.com/config/ubuntu/19.10/prod.list > /etc/apt/sources.list.d/mssql-release.list

exit
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install msodbcsql17
sudo ACCEPT_EULA=Y apt-get install mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
sudo apt-get install unixodbc-dev
```

Get all unixODBC information
> odbcinst -j

Get Driver Information:
> cat /etc/odbcinst.ini

#### Windows

The driver is installed when you run `msodbcsql.msi` from one of the downloads for Windows from the following link:

https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15#download-for-windows

## Running Locally

#### Run Django Server

> python manage.py runserver


#### Run Redis Server

> redis-server


#### Run Celery Worker

> celery -A smart_ai worker -l info


#### Run Celery Beat

> celery -A smart_ai beat -l info


# Running celery as a service using NSSM on windows

> Non Sucking Service Manager (NSSM) can be downloaded from http://nssm.cc/download

> Add the exe file to the project directory besides manage.py

> Open the cmd in the directory and execute the command: `nssm install service_name`

> An interface should pop up for service creation. In the application tab, provide the 
> `path` for the python executable location in your virtual environment, project directory 
> as the `startup directory`, and celery commands as `arguments`.  

> You can also specify the path for log file against output and error under I/O tab. 

> Once the service is created, you can locate it under task manager in order to start/stop 
> the service. You can also use NSSM commandline to do the same.  

> More information on https://www.programmersought.com/article/4425103991/ 
> and http://nssm.cc/usage 

> NSSM Commands: http://nssm.cc/commands


# ToDo: Multiple Celery Queue using kombu Exchange & Queue

https://github.com/msthakkar121/plaid_rest_celery

Changes in 
* base.py 
    ```
    # Celery configurations
    CELERY_TASK_CREATE_MISSING_QUEUES = True
    
    # Don't use pickle as serializer, json is much safer
    CELERY_TASK_SERIALIZER = "json"
    CELERY_ACCEPT_CONTENT = ['application/json']
    
    # CELERY ROUTES (Register all the tasks present in the project and specify their respective queues)
    CELERY_TASK_ROUTES = {
        'appname.tasks.taskname': {'queue': 'queue1'},
        'appname.tasks.taskname': {'queue': 'queue1'},
        'appname.tasks.taskname': {'queue': 'queue2'},
        'appname.tasks.taskname': {'queue': 'queue2'},
    }  
  ```
* celery.py
    ```
    ...
    from kombu import Exchange, Queue
  
    exchange1 = Exchange('queue1', type='direct')
    exchange2 = Exchange('queue2', type='direct')
    
    app.conf.task_queues = (
        Queue('queue1', exchange1, routing_key='queue1'),
        Queue('queue2', exchange2, routing_key='queue2')
    )
    
    app.conf.task_default_queue = 'queue1'
    app.conf.task_default_exchange = 'queue1'
    app.conf.task_default_routing_key = 'queue1'
    ...
  ```
* tasks.py
    ```
    from appname.celery import app
    
    # change task decorators to @app.task 
  ```
