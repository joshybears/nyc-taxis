# nyc-taxis

## Project Overview

### Description
`nyc-taxis` is a small ETL project that gets Yellow Taxi Trip record data from the NYC Taxi & Limousine Commission website (https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page), uploads it onto a Postgres DB, and allows visualization of the data via Jupyter Notebook. 

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
Files & Folders:
- Pipfile
  - Lists out Python dependencies and libraries, for use with Pipenv
- README.md
  - Description and directions for the project
- docker-compose.yml
  - Lists out services to be run with Docker
- etl
  - Contains ingestion scripts
- images
  - Contains images for embed in GH repo
- notebooks
  - Contains notebooks for use with Jupyter
- pgdb
  - Mount point for Postgres DB (generated upon running docker compose)
- tmp
  - Temporary file storage

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

### View Visualization
1. In the main directory, run the following command to run jupyter notebook: `pipenv run jupyter notebook`
2. Open file `notebooks/Yellow-Taxi-Analysis.ipynb` using Jupyter
3. Run all the modules, the visualization should appear after some time
4. Check the visualization, feel free to modify the query dates, modify the chart

## Discussion

### Assumptions
- We take only the newer file format that the site provides (Parquet), which means files from 2015 onwards
- We assume the same URL structure for all of the files `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{date_string}.parquet`
- We exclude 0 and NaN values for field passenger_count from ingestion
- Pipeline can be run for the same date multiple times (idempotence)
  - We detect presence of the table and indexes to make sure it's there before doing any writing (prep_db function)
  - We use the URL to avoid duplicates, we delete first any entries with the current URL before writing (using append)
- We have to use a date filter when getting data, because some files contain dates not from that month

### Personal Challenges
- Choosing technologies
  - I found it challenging to choose which technologies would be appropriate for this project, because there are so many ways to do things. Ultimately stuck with what I know/commonly use and what could stand on its own, although I can think of other possible more sophisticated platforms and solutions for this exercise.
- Unfamiliarity with Jupyter graphs & plots
  - I learned a bit of Jupyter graphing/plotting during my time with Eskwelabs (Data Science Bootcamp), but I can't say I'm super proficient with it. Had to go back, reread lessons, and consult online resources to relearn how to do pandas/matplotlib graphing.

### Data & Conclusions

See below graph for sum of total amount per day (using pickup time as the effective date):

![Data for 2023 December](/images/viz.png)

Looking at the data, we can see peak ridership during latter half of the weekdays (Wed-Fri) during the first two weeks of December (Dec 6, 7, 8; Dec 13, 14, 15). Total amounts add up to almost 4 million for these dates.
However the numbers go way down during the holiday season, with Dec 25 recording the lowest value at just 1.2M. Days adjacent to Christmas and New Year's Eve follow this.
With more analysis, I am sure many more interesting points and trends can be seen.

See below table for an ordered list of sums of total amounts per date:

![Biggest total amounts for 2023 December](/images/max_amounts.png)

