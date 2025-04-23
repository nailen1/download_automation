import os
import time
import math
import pandas as pd
import numpy as np
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from shining_pebbles import *
from aws_s3_controller import *
from dotenv import load_dotenv
from tqdm import tqdm
from .consts import *

client = MongoClient(MY_MONGO_URI)
# db = client[LEGACY_DATABASE_NAME]

def create_database(database_name):
    db = client[database_name]
    collection = db[f'hello-{database_name}']
    collection.insert_one({'text': f'hello-{database_name}!'})
    print(f'- Created database {database_name}.')
    return None

def get_collection_names_includes_something_in_database(database_name, something):
    db = client[database_name]
    collection_names = [collection_name for collection_name in db.list_collection_names() if something in collection_name]
    return collection_names

def get_index_collection_names(database_name=LEGACY_DATABASE_NAME):
    collection_names = get_collection_names_includes_something_in_database(database_name, ' Index')
    return collection_names

def set_date_as_unique_index(collection_name, key_for_date):
    db = client[LEGACY_DATABASE_NAME]
    try:
        db[collection_name].create_index([(key_for_date, pymongo.ASCENDING)], unique=True)
    except Exception as e:
        print(e)
        return

def insert_data_to_database_collection(database_name, collection_name, data):
    db = client[database_name]
    collection = db[collection_name]

    bucket_insert_done = []
    bucket_insert_fail = []
    n = len(data)
    for i, datum in enumerate(data):
        print(f'- try insert {i+1}/{n} data in {database_name}.{collection_name} ...')
        try:
            collection.insert_one(datum)
            bucket_insert_done.append(datum)
            print(f'-- done: {datum}')
        except Exception as e:
            bucket_insert_fail.append(datum)
            print(f'-- fail: {datum}, error: {e}')

    return bucket_insert_done, bucket_insert_fail

def set_compound_unique_index(database_name, collection_name, keys):
    db = client[database_name]
    collection = db[collection_name]
    collection.create_index(
        [(key, pymongo.ASCENDING) for key in keys],
    unique=True
    )
    print(f'Compound unique index set for {keys} in {database_name}.{collection_name}')
    return

def insert_many_data_with_no_duplicates(database_name, collection_name, data):
    db = client[database_name]
    collection = db[collection_name]
    from pymongo.errors import BulkWriteError
    try:
        collection.insert_many(data, ordered=False)
    except BulkWriteError as e:
        print(f"Inserted {e.details['nInserted']} documents")
        print(f"Encountered {len(e.details['writeErrors'])} duplicate key errors")
    return

def insert_index_prices_from_S3_to_mongodb(ticker_bbg):
    df = open_df_in_bucket_by_regex(bucket='dataset-bbg', bucket_prefix='dataset-index', regex=ticker_bbg)
    data = df.to_dict('records')
    done, fail = insert_data_to_database_collection(database_name=LEGACY_DATABASE_NAME, collection_name=f'timeseries-{ticker_bbg}', data=data)
    return done, fail

def insert_every_index_price_to_collections():
    collection_names_index = get_index_collection_names()
    tickers_bbg = [collection_name.replace('timeseries-', '') for collection_name in collection_names_index]
    for ticker_bbg in tickers_bbg:
        insert_index_price_from_S3_to_mongodb(ticker_bbg)
    return

def open_every_df_menu2160_in_s3(start_date, end_date, save_date):
    dct = {}
    file_keys = scan_files_in_bucket_by_regex(bucket='dataset-system', bucket_prefix=f'dataset-timeseries-menu2160-from{start_date}-to{end_date}-save{save_date}', regex='')
    for i, file_key in enumerate(file_keys):
        fund_code = pick_n_characters_followed_by_something_in_string(string=file_key, something='code', n=6)
        df_menu2160 = open_df_in_bucket(bucket='dataset-system', file_key=file_key)
        dct[fund_code] = df_menu2160
    return dct

def preprocess_every_dataset_menu2160_in_s3(start_date, end_date, save_date, ):
    dct = {}
    dct_dfs = open_every_df_menu2160_in_s3(start_date, end_date, save_date)
    for code, df in dct_dfs.items():
        df = preprocess_to_extract_timeseries_price_in_menu2160(df)
        dct[code] = df 
    return dct


def insert_every_timeseries_fund_to_database():
    dct = preprocess_every_dataset_menu2160_in_s3()
    n = len(dct.keys())
    for i, (fund_code, df) in enumerate(dct.items()):
        print(f'- ({i}/{n}) inserting timeseries to database: {fund_code}')
        data = df.to_dict(orient='records')
        insert_data_to_database_collection(database_name=LEGACY_DATABASE_NAME, collection_name=f'timeseries-{fund_code} Fund', data=data)



### DATAFRAME MAKER

def get_dct_timeseries(family='Fund'):
    dct = {}
    names = get_collection_names_includes_something_in_database(LEGACY_DATABASE_NAME, family)
    for name in names:
        key = name.replace('timeseries-', '')
        collection = db[name]
        data = list(collection.find({},{'_id': 0}))
        dct[key] = data
    return dct

def get_df_prices(family='Fund'):
    dct = get_dct_timeseries(family)
    bucket = []
    for k,v in dct.items():
        df = pd.DataFrame(v).set_index('date')
        df.columns = [k]
        bucket.append(df)
    df_prices = pd.concat(bucket, axis=1).sort_index(ascending=True, axis=0).sort_index(ascending=True, axis=1).fillna(value=0)
    df_prices['LIFEAM Fund'] = df_prices.sum(axis=1)
    return df_prices


### FUND PRICE TIMESERIES MAKER 
### REF: KB MOS 
# SP 또는 LAM 으로 이동할것
def preprocess_timeseries(df, time_col_from, value_col_from, time_col_to, value_col_to):
    print('-step 1: drop NaN')
    df = df[[time_col_from, value_col_from]].dropna()
    print('-step 2: rename columns to date and price')
    df = df.rename(columns={time_col_from: time_col_to, value_col_from: value_col_to})
    print('-step 3: reset index')
    df = df.reset_index(drop=True)
    df = df.copy()
    try:
        print('-step 4: convert value to float type')
        df[value_col_to] = df[value_col_to].str.replace(',', '').astype(float)
    except Exception as e:
        print(e)
    return df


def preprocess_to_extract_timeseries_price_in_menu2160(df_menu2160):
    df = preprocess_timeseries(df_menu2160, time_col_from='일자', value_col_from='수정\n기준가', time_col_to='date', value_col_to='price')
    return df

def preprocess_to_extract_timeseries_nav_in_menu2160(df_menu2160):
    df = preprocess_timeseries(df_menu2160, time_col_from='일자', value_col_from='순자산총액', time_col_to='date', value_col_to='nav')
    return df

def preprocess_timeseries_for_multicolumns(df, time_col_from, value_cols_from, time_col_to, value_cols_to):
    print('-step 1: drop NaN')
    df = df[[time_col_from, *value_cols_from]].dropna()
    print('-step 2: rename columns to date and price')
    df.columns = [time_col_to, *value_cols_to]
    print('-step 3: reset index')
    df = df.reset_index(drop=True)
    df = df.copy()
    try:
        print('-step 4: convert value to float type')
        for col in value_cols_to:
            df[col] = df[col].str.replace(',', '').astype(float)
    except Exception as e:
        print(e)
    return df

def preprocess_timeseries_of_menu2160_for_multicolumns(df_menu2160):
    df = preprocess_timeseries_for_multicolumns(df_menu2160, time_col_from='일자', value_cols_from=['수정\n기준가', '순자산총액'], time_col_to='date', value_cols_to=['price', 'nav'])
    return df


def get_fund_data_from_mongodb(fund_code, key):
    db = client[LEGACY_DATABASE_NAME]
    collection = db['data-menu2160']
    data = list(collection.find({'펀드': fund_code}, {'일자': 1, key: 1, '_id': 0}))
    return data


def upload_bbg_index(database_name, collection_name):
    ticker_bbg_index = collection_name.split('bbg-')[-1]
    category = ticker_bbg_index.split(' ')[-1]
    db = client[database_name]
    collection = db[collection_name]
    last_document = collection.find().sort("date", pymongo.DESCENDING).limit(1)[0]
    last_date = last_document['date']
    mapping_file_subfolder ={
        'Index': 'dataset-index',
        'Curncy': 'dataset-currency',
    }
    # file_subfolder = mapping_file_subfolder[category]
    # file_folder = os.path.join(BASE_DIR_FUND, file_subfolder)
    # df = open_df_in_file_folder_by_regex(file_folder=file_folder, regex=ticker_bbg_index)
    bucket_prefix_bbg = mapping_file_subfolder[category]
    df = open_df_in_bucket_by_regex(bucket='dataset-bbg', bucket_prefix=bucket_prefix_bbg, regex=ticker_bbg_index)
    df = df[df.index > last_date]
    if df.shape[0] == 0:
        print(f'-- no new data for {ticker_bbg_index}')
        return 
    df = df[df.index != get_today("%Y-%m-%d")]
    data = df.reset_index().to_dict(orient='records')
    done, fail = insert_data_to_database_collection(database_name=database_name, collection_name=collection_name, data=data)
    return fail


def upload_every_bbg_index(database_name=LEGACY_DATABASE_NAME):
    db = client[database_name]
    collection_names = db.list_collection_names()
    for collection_name in collection_names:
        if ' Index' in collection_name or ' Curncy' in collection_name:
            print(f'- uploading {collection_name}')
            upload_bbg_index(database_name=database_name, collection_name=collection_name)


def upload_all_menu2160_snapshots_to_mongodb(database_name, collection_name, start_date='20200526', end_date=None):
    end_date = get_date_n_days_ago(get_today("%Y%m%d"), 1) if end_date is None else end_date
    dates = get_date_range(start_date_str=start_date, end_date_str=end_date, form="%Y%m%d")
    dates = sorted(dates, reverse=True)
    for date in tqdm(dates):
        df = open_df_in_bucket_by_regex(bucket='dataset-system', bucket_prefix='dataset-menu2820-snapshot', regex=f'at{date}')
        data = df.reset_index().to_dict(orient='records')[1:]
        insert_data_to_database_collection(database_name=database_name, collection_name=collection_name, data=data)


# DataFrames to be migrated from files system to MongoDB

def get_df_index_from_mongodb(ticker_bbg_index):
    database = client[LEGACY_DATABASE_NAME]
    collection = database[f'data-bbg-{ticker_bbg_index}']
    data = list(collection.find({},{'_id': 0}))
    df = pd.DataFrame(data)
    df = df.rename(columns={'PX_LAST': ticker_bbg_index.split(' Index')[0]})
    return df

def get_df_currency_from_mongodb(ticker_bbg_currency):
    database = client[LEGACY_DATABASE_NAME]
    collection = database[f'data-bbg-{ticker_bbg_currency}']
    data = list(collection.find({},{'_id': 0}))
    df = pd.DataFrame(data)
    df = df.rename(columns={'PX_LAST': ticker_bbg_currency.split(' Curncy')[0]})
    return df

def get_df_menu2160(fund_code):
    database = client[LEGACY_DATABASE_NAME]
    collection = database[f'data-menu2160-snapshot']
    data = list(collection.find({'펀드': fund_code},{'_id': 0, 'index':0}))
    df = pd.DataFrame(data)
    return df


def get_data_funds_prices():
    database = client[LEGACY_DATABASE_NAME]
    collection = database['data-menu2160-snapshot']
    data = list(collection.find({}, {
    '일자': 1,
    '펀드': 1,
    '수정\n기준가': 1,
    '_id': 0 
    }))
    df = pd.DataFrame(data).pivot(index='일자', columns='펀드', values='수정\n기준가')
    for col in df.columns:
        df[col] = df[col].str.replace(',', '').astype(float)
    df.columns = [f'price_{fund_code}' for fund_code in df.columns]
    df.columns.name = None
    df.index.name = 'date'

    kospi = get_df_index_from_mongodb('KOSPI Index').set_index('date')
    df = df.merge(kospi, how='left', left_index=True, right_index=True)

    data = df.reset_index().ffill().to_dict(orient="list")
    for key, value in data.items():
        data[key] = [None if isinstance(v, float) and math.isnan(v) else v for v in value]    

    return data


# insert fund data to mongodb

def get_data_menu2160_snapshot_at(input_date, data_lake='aws'):
    if data_lake == 'aws':
        df = open_df_in_bucket_by_regex(bucket='dataset-system', bucket_prefix='dataset-menu2160-snapshot', regex=f'at{input_date.replace("-", "")}')
    elif data_lake == 'local':
        df = open_df_in_file_folder_by_regex(file_folder='dataset-menu2160-snapshot',regex=f'at{input_date.replace("-", "")}')
    df['펀드'] = df['펀드'].apply(lambda x: f"{int(float(x)):06d}" if pd.notna(x) and str(x).replace('.', '').isdigit() else str(x).zfill(6))
    data = df.iloc[1:, :].reset_index().to_dict(orient='records')
    return data        

def insert_datum_menu2160_snapshot_to_mongodb(database_name, collection_name, input_date):
    input_date = input_date.replace('-', '')
    data = get_data_menu2160_snapshot_at(input_date)
    database = client[database_name]
    collection = database[collection_name]
    try:
        collection.insert_many(data)
        print(f'⭕ insert datum {input_date}')
        return None
    except Exception as e:
        current_unix_time = int(time.time())
        print(f'❌ insert datum {input_date} failed')
        print(e)
        return {'input_date': input_date,'update_time': current_unix_time, 'error': e}
    

def insert_data_menu2160_snapshot_to_mongodb(database_name, collection_name, input_dates=None):
    if input_dates == None:
        file_names_in_bucket = scan_files_in_bucket_by_regex(bucket='dataset-system', bucket_prefix='dataset-menu2160-snapshot', regex='menu2160-code000000')
        input_dates_in_bucket = [pick_input_date_in_file_name(file_name) for file_name in file_names_in_bucket]
        input_dates = input_dates_in_bucket
    input_dates = sorted(input_dates, reverse=True)
    errors = []
    for input_date in tqdm(input_dates):
        result = insert_datum_menu2160_snapshot_to_mongodb(database_name=database_name, collection_name=collection_name, input_date=input_date)
        if result != None:
            errors.append(result)
    df_errors = pd.DataFrame(errors)
    save_dataset_of_subject_at(df=df_errors, file_folder='dataset-log', subject='insert_errors', input_date=get_today("%Y%m%d"))
    return df_errors
    