from download_automation import Activator
from menu_downloader import wait_for_n_seconds
from shining_pebbles import get_date_range, get_yesterday
from datetime import datetime
from tqdm import tqdm
from menu_downloader import MOS1100, MAPPING_PSEUDO_CODES, DATALAKE_DIR, FILE_FOLDER
from string_date_controller import get_yesterday
from shining_pebbles import get_date_range
from shining_pebbles import extract_dates_ref_in_file_folder_by_regex
import os
from mongodb_controller import client

# activator = Activator()
# activator.on_mos()

dates = get_date_range(start_date_str='2020-01-01', end_date_str=get_yesterday())[::-1]
file_folder = os.path.join(DATALAKE_DIR, FILE_FOLDER('1100'))
get_dates_local_by_code = lambda pseudo_code: extract_dates_ref_in_file_folder_by_regex(file_folder=file_folder, regex=f'code{pseudo_code}-at')
get_collection = lambda pseudo_code: client['database_rpa'][f'dataset-menu1100-{pseudo_code}']
get_dates_db_by_code = lambda pseudo_code: get_collection(pseudo_code).distinct('일자')

for date in tqdm(dates):

    current_hour = datetime.now().hour
    if 2 <= current_hour < 6:
        print(f"Current time is {current_hour}:00 (past 2 AM). Stopping the loop.")        
        break
    print(f"# Downloading data for date: {date}")

    for menu_code, pseudo_code in MAPPING_PSEUDO_CODES.items():
        dates_local = get_dates_local_by_code(pseudo_code=pseudo_code)
        dates_db = get_dates_db_by_code(pseudo_code=pseudo_code)
        dates_to_download = sorted(list((set(dates) - set(dates_local)) - set(dates_db)), reverse=True)
        if date in dates_to_download:
            mos = MOS1100(menu_code=menu_code, start_date=date, end_date=date)
            mos.recursive_download_dataset()
            wait_for_n_seconds(1)
