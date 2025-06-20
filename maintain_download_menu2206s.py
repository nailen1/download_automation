from download_automation import Activator
from menu_downloader import MOS2206, wait_for_n_seconds
from shining_pebbles import get_date_range, get_yesterday
from mongodb_controller import COLLECTION_2206
from datetime import datetime
from tqdm import tqdm
from database_managing.insert_applications.s3_application import upload_nonexisting_menu_files_to_bucket
from database_managing import Menu2206s

activator = Activator()
activator.on_mos()

activator.on_mos()
dates = get_date_range(start_date_str='2021-01-01', end_date_str=get_yesterday())
# dates = get_date_range(start_date_str='2021-01-01', end_date_str='2025-04-21')

dates_in_db = COLLECTION_2206.distinct('일자')
dates_to_download= sorted(list(set(dates) - set(dates_in_db)), reverse=True)

for date in tqdm(dates_to_download):
    current_hour = datetime.now().hour
    # 새벽 2시~6시 사이에만 종료 (다음날 새벽 2시)
    if 2 <= current_hour < 6:
        print(f"Current time is {current_hour}:00 (past 2 AM). Stopping the loop.")        
        break
    print(f"# Downloading data for date: {date}")

    mos = MOS2206(date_ref=date)
    mos.execute_all_sequences()

    upload_nonexisting_menu_files_to_bucket(menu_code='2206')

    m = Menu2206s()
    m.fetch_snapshots()
    m.insert_all()

    wait_for_n_seconds(5)
