import json
import pandas as pd
from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator

default_args = {
    'owner' : 'airflow',
    'depend_on_past': False,
    'start_date' : datetime(2023,8,2),
    'email': ['email@domain.com'],
    'email_on_failure': False,
    'retries': 1,
    'retry_delay' : timedelta(minutes=5)
}

with DAG(
        'stock_data_dag',
        default_args = default_args,
        schedule_interval = '@daily',
        catchup = False    
        ) as dag:

        is_stock_api_ready = HttpSensor(
        task_id = 'is_stock_api_ready',
        http_conn_id = 'stock_data_api',
        endpoint = '/query?function=TIME_SERIES_DAILY&symbol=AMZN&apikey=[YOUR_API_KEY]'
        )

        extract_stock_data = SimpleHttpOperator(
        task_id = 'extract_stock_data',
        http_conn_id = 'stock_data_api',
        endpoint = '/query?function=TIME_SERIES_DAILY&symbol=AMZN&apikey=[YOUR_API_KEY]', 
        method = 'GET', 
        response_filter = lambda r:json.loads(r.text),
        log_response = True      
        )

        is_stock_api_ready >> extract_stock_data 



