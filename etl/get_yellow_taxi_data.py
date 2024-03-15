import argparse
import datetime
import pandas
import pyarrow
import requests
import shutil
import sqlalchemy

FIELDS = [
    'VendorID', 
    'tpep_pickup_datetime', 
    'tpep_dropoff_datetime', 
    'passenger_count', 
    'trip_distance', 
    'RatecodeID', 
    'store_and_fwd_flag', 
    'PULocationID', 
    'DOLocationID', 
    'payment_type', 
    'fare_amount', 
    'extra', 
    'mta_tax', 
    'tip_amount', 
    'tolls_amount', 
    'improvement_surcharge', 
    'total_amount', 
    'congestion_surcharge', 
    'Airport_fee'   
]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', required = True)
    parser.add_argument('--month', required = True)
    args = parser.parse_args()

    year = int(args.year)
    month = int(args.month)

    # support 2015 - 2023 (parquet format)
    if year < 2015 or year > 2023:
        raise Exception('Year must be 2015 - 2023.')
    # if month < 1 or month > 12:
    #     raise Exception('Month must be 1 - 12.')

    return datetime.datetime(year, month, 1)

def get_data(url):

    local_filename = f'''tmp/{url.split('/')[-1]}'''
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    df = pandas.read_parquet(local_filename, columns=FIELDS, engine='pyarrow')

    # remove NaN values
    df = df[df['passenger_count'].notnull()]

    # remove 0 values
    df = df[df['passenger_count'] != 0]

    df['url'] = url
    print(df)
    print(df.shape)
    print(df.columns.tolist())

    return df

def prep_db(engine, url):

    query = f'''
    CREATE TABLE IF NOT EXISTS public.yellow_taxis (
        "VendorID" int4 NULL,
        tpep_pickup_datetime timestamp NULL,
        tpep_dropoff_datetime timestamp NULL,
        passenger_count float8 NULL,
        trip_distance float8 NULL,
        "RatecodeID" float8 NULL,
        store_and_fwd_flag text NULL,
        "PULocationID" int4 NULL,
        "DOLocationID" int4 NULL,
        payment_type int8 NULL,
        fare_amount float8 NULL,
        extra float8 NULL,
        mta_tax float8 NULL,
        tip_amount float8 NULL,
        tolls_amount float8 NULL,
        improvement_surcharge float8 NULL,
        total_amount float8 NULL,
        congestion_surcharge float8 NULL,
        "Airport_fee" float8 NULL,
        url text NULL
    );
    CREATE INDEX IF NOT EXISTS yellow_taxis_url_idx ON public.yellow_taxis USING btree (url);
    DELETE FROM yellow_taxis WHERE url = '{url}';
    '''
    with engine.begin() as conn:
        conn.exec_driver_sql(query)
    print('DB is prepped!')

def write_to_db(engine, data):
    data.to_sql('yellow_taxis', con=engine, if_exists='append', index=False)

if __name__ == '__main__':

    date = parse_args()

    date_string = date.strftime('%Y-%m')
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{date_string}.parquet'
    data = get_data(url)
    engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:postgres123@localhost/nycdata')
    prep_db(engine, url)
    write_to_db(engine, data)
