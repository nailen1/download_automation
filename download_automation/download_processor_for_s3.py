# download_processor_for_s3.py
# S3 UPLOAD GENERAL

from shining_pebbles import *
from aws_s3_controller import *
import pandas as pd

def validate_download_process(file_folder, file_name, exception=False):
    print(f'- step: validate download process.')
    if exception:
        return True
    df = open_df_in_file_folder_by_regex(file_folder=file_folder, regex=file_name)
    shape = df.iloc[:, :2].dropna().shape
    rows = shape[0]
    print(f'-- {rows} rows in dataset.')
    if rows > 0:
        print(f'⭕: download complete.')
        return True
    else:
        print(f'❌: download failed.')
        return False
    

def upload_downloaded_dataset_to_s3(file_folder, file_name, bucket_prefix, bucket='dataset-system'):
    upload_files_to_s3(file_folder_local=file_folder, regex=file_name, bucket=bucket, bucket_prefix=bucket_prefix)
    print(f'🪣: uploading dataset to S3://{bucket}/{bucket_prefix} complete.')


def get_df_fundlist_from_menu2160_snapshots_in_s3(input_date=None, category='all'):
    if input_date:
        df = open_df_in_bucket_by_regex(bucket='dataset-system', bucket_prefix='dataset-menu2160-snapshot', regex=f'menu2160-code000000-at{input_date}')
    df = open_df_in_bucket_by_regex(bucket='dataset-system', bucket_prefix='dataset-menu2160-snapshot', regex='menu2160-code000000')
    ref_date = df.reset_index().iloc[-1]['일자']
    df = df[['펀드명', '펀드']].iloc[1:, :].set_index('펀드')
    df.index.name = '펀드코드'
    df.columns.name = ref_date
    df_fund = df[~df['펀드명'].str.contains('Class')]
    fund_codes_flagship = ['100004', '100019', '100030', '100060']
    df_fund_flagship = df_fund[df_fund.index.isin(fund_codes_flagship)]
    df_fund_nonflagship = df_fund[~df_fund.index.isin(fund_codes_flagship)].sort_index()
    df_fund = pd.concat([df_fund_flagship, df_fund_nonflagship], axis=0)
    df_class_fund = df[df['펀드명'].str.contains('Class')]
    if category == 'all':
        df = pd.concat([df_fund, df_class_fund], axis=0)
    elif category == 'fund':
        df = df_fund
    elif category == 'class':
        df = df_class_fund

    return df