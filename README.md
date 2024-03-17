# nyc-taxis

## Project Overview

### Folder Structure
```
nyc-taxis
├── Pipfile
├── README.md
├── docker-compose.yml
├── etl
│   └── get_yellow_taxi_data.py
├── images
│   └── viz.png
├── notebooks
│   └── Yellow-Taxi-Analysis.ipynb
├── pgdb
└── tmp
```

## Setup Instructions

### Setup Postgres DB
In this project, we use PostgreSQL as our database service. We use Docker to containerize the database as well.
1. Make sure you have Docker installed (https://www.docker.com/products/docker-desktop/)
2. Simply run `docker compose up` in the main directory
   - This will pull the Postgres docker image and run it within a container on your system

### Setup Pipenv
In this project, we use Pipenv to install Python dependencies that we need, for both our ETL script and the visualization tool we use (Jupyter notebook).
1. Make sure you have Pipenv installed (https://pipenv.pypa.io/en/latest/installation.html)
2. Simply run `pipenv install` in the main directory
   - This will install all the libraries and dependencies that the project needs according to the Pipfile

## Execution Instructions

### Execute ETL
1. In the main directory, run the following command (don't forget to change year and month): `pipenv run python etl/get_yellow_taxi_data.py --year <year> --month <month>`
   - STDOUT will show the progress.
   - Supported years: 2015 - 2023 (this is the period that they used the parquet files)
   - STDOUT will show the progress.

### View Visualization
1. In the main directory, run the following command to run jupyter notebook: `pipenv run jupyter notebook`
2. Open file `notebooks/Yellow-Taxi-Analysis.ipynb` using Jupyter
3. Run all the modules, the visualization should appear after some time
4. Check the visualization, feel free to modify the query dates, modify the chart

## Discussion

![Data for 2023 December](/images/viz.png)
