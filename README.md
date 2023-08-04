# Stock Market Data Ingestion using Airflow Project
## Introduction
This is an end-to-end data engineering project which ingest stock market data from AlphaVantage API using Python & Airflow. The data is transformed and stored in S3 bucket which can be queried using Athena for analytical use case

### Technologies Used:
* **AWS Cloud (EC2, S3, Athena)**: EC2 is used to host Airflow webserver, S3 is used a a storage solution, Athena for querying purposes
* **Apache Airflow** : Airflow is used as an orchestration layer to monitor and manage workflows through DAGs
* **Python** : Python is used to specify the logic to extract, transform and load data from API 

## Architecture
![Stock_Airflow](https://github.com/keerthanakumar1510/stock-data-airflow-data-engineering/assets/70489416/538f7835-aeb2-4986-98c6-1d3bb358b7d4)

## Alpha Vantage API
Alpha Vantage provides realtime and historical financial market data through a set of powerful and developer-friendly data APIs. In this project, I have used **TIME_SERIES_DAILY API** which returns raw (as-traded) daily time series (date, daily open, daily high, daily low, daily close, daily volume) of the global equity specified: Amazon (AMZN) is the equity of interest in this project

* Sign up and get your free API key: https://www.alphavantage.co/support/#api-key
* API Documentation: https://www.alphavantage.co/documentation/

## Pre-requisites
* EC2 instance: Instance type atleast t2.small or greater, OS image: Ubuntu
* Airflow installation: Follow **required-packages.sh** file for the commands

## Reference
1. https://airflow.apache.org/docs/apache-airflow-providers-http/stable/_api/airflow/providers/http/sensors/http/index.html
2. https://airflow.apache.org/docs/apache-airflow-providers-http/stable/_api/airflow/providers/http/operators/http/index.html
3. https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html



