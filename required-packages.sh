## Install the following packages
sudo apt update
sudo apt install python3-pip
sudo apt install python3.10-venv

## Creating a virtual environment
python3 -m venv airflow_venv

## Activate virtual environment
source airflow_venv/bin/activate

## Install Dependencies
sudo pip install pandas
sudo pip install s3fs

## Install airflow
sudo pip install apache-airflow

## Starting airflow
airflow standalone
