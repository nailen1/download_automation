from menu_downloader import MOS1100, MAPPING_PSEUDO_CODES
from string_date_controller import get_yesterday, get_first_date_of_month, get_date_n_months_ago, get_date_n_days_after
from mongodb_controller import client
from database_managing.insert_utils import insert_menu1100_alternative

def get_first_date_of_past_month(date):
    date = get_date_n_months_ago(date, 1)
    return get_first_date_of_month(date) 

end_date = get_yesterday()
start_date = get_first_date_of_past_month(end_date)

def delete_data_to_correct_in_menu1100_collection(ticker_pseudo, start_date, end_date):
    collection = lambda ticker_pseudo: client['database-rpa'][f'dataset-menu1100-{ticker_pseudo}']
    pipeline = [
        {
            '$match': {
                '일자': {
                    '$gte': start_date,
                    '$lte': end_date
                }
            }
        },
    ]
    cursor = collection(ticker_pseudo).aggregate(pipeline)
    data = list(cursor)
    print(f"Deleting {len(data)} documents from {ticker_pseudo} collection between {start_date} and {end_date}.")
    for doc in data:
        collection(ticker_pseudo).delete_one({'_id': doc['_id']})
    cursor = collection(ticker_pseudo).aggregate(pipeline)
    data = list(cursor)
    print(f"After deletion, {len(data)} documents remain in {ticker_pseudo} collection.")
    return data

for menu_code, ticker_pseudo in MAPPING_PSEUDO_CODES.items():
    mos = MOS1100(menu_code=menu_code, start_date=start_date, end_date=end_date)
    mos.recursive_download_dataset()
    delete_data_to_correct_in_menu1100_collection(ticker_pseudo=ticker_pseudo, start_date=start_date, end_date=end_date)
    insert_menu1100_alternative(ticker_pseudo=ticker_pseudo, start_date=start_date, end_date=end_date)
