from shining_pebbles import get_yesterday
from aws_s3_controller import open_df_in_bucket_by_regex
from .database_utils import insert_data_to_database_collection
from .consts import LEGACY_DATABASE_NAME

def insert_raw_menu2160_snapshot_to_database(date_ref=None):
    date_ref = date_ref or get_yesterday()
    BUCKET_PREFIX_FOR_MENU2160_SNAPSHOT = 'dataset-menu2160-snapshot'
    COLLECTION_NAME_FOR_MENU2160_SNAPSHOT = 'data-menu2160-snapshot'
    df_raw = open_df_in_bucket_by_regex(bucket='dataset-system', bucket_prefix=BUCKET_PREFIX_FOR_MENU2160_SNAPSHOT, regex=f'at{date_ref.replace("-", "")}')
    data = df_raw.reset_index().to_dict(orient='records')[1:]
    insert_data_to_database_collection(database_name=LEGACY_DATABASE_NAME, collection_name=COLLECTION_NAME_FOR_MENU2160_SNAPSHOT, data=data)
    return None
