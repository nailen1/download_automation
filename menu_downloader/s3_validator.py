from shining_pebbles import *
from aws_s3_controller import *

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
