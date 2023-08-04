import json
import pandas as pd
from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator

def transform_load_data(task_instance):
    #Referring to extract task id for fetching data
    data = task_instance.xcom_pull(task_ids = 'extract_stock_data')
    #Converting to a dataframe
    stock_data = pd.DataFrame(data['Time Series (Daily)']).T
    stock_data.reset_index(inplace=True)
    #Renaming field names
    amzn_data = stock_data.rename(columns = {'index' : 'Date', '1. open' : 'Open', '2. high' : 'High', '3. low' : 'Low', '4. close' : 'Close', '5. volume' : 'Volume'})
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d")
    #writing the data to S3 bucket
    amzn_data.to_csv(f"s3://stock-data-from-vantage-api/amzn_{dt_string}.csv", index = False)

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

        transform_load_stock_data = PythonOperator(
        task_id = 'transform_load_stock_data',
        python_callable = transform_load_data
        )

        is_stock_api_ready >> extract_stock_data >> transform_load_stock_data 



