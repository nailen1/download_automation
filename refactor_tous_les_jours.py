import schedule
import time
from datetime import datetime, timedelta
import argparse
from download_automation import *
# from database_managing.insert_utils.menu2206 import Menu2206s
from database_managing import *
from tqdm import tqdm
from menu_downloader import MOS2206, MOS1100, MAPPING_PSEUDO_CODES, DATALAKE_DIR
from mongodb_controller import client

def run_download_tasks():
    date_ref = get_yesterday()
    activator = Activator()

    activator.on_bos()
    download_all_snapshot_datasets_of_timeseries(menu_code='8186', end_date=date_ref)
    menu_fetcher = Menu8186Snapshots()
    menu_fetcher.fetch_snapshots()
    menu_fetcher.insert_all()

    activator.on_mos()

    m = MOS2206(date_ref=date_ref)
    m.recursive_download_dataset()
    menu2206_fetcher = Menu2206s()
    menu2206_fetcher.fetch_snapshots()
    menu2206_fetcher.insert_all()


    download_menu2205s_priority_1(date_ref=date_ref)
    dates_and_codes = get_nonexisting_pairs_date_code_for_menu2205()
    for date, code in tqdm(dates_and_codes):
        if date == date_ref:
            menu2205_fetcher = Menu2205(fund_code=code, date_ref=date)
            menu2205_fetcher.fetch_unit_df()
            menu2205_fetcher.insert_unit()

    mos = OfficeSystem(menu_code='2110', input_date=date_ref)
    mos.recursive_download_dataset()
    insert_every_menu_data()
    
    download_menu2205s_priority_2(date_ref=date_ref)
    dates_and_codes = get_nonexisting_pairs_date_code_for_menu2205()
    for date, code in tqdm(dates_and_codes):
        if date == date_ref:
            m = Menu2205(fund_code=code, date_ref=date)
            m.fetch_unit_df()
            m.insert_unit()


    activator.on_mos()
    MOS_MENU_CODES_FOR_FUND_INFO = ['2110', '3412']
    for menu_code in tqdm(MOS_MENU_CODES_FOR_FUND_INFO):
        mos = OfficeSystem(menu_code=menu_code, input_date=date_ref)
        mos.recursive_download_dataset()

    activator.on_bos()
    BOS_MENU_CODES_FOR_FUND_INFO = ['3421', '3233']
    for menu_code in tqdm(BOS_MENU_CODES_FOR_FUND_INFO):
        bos = OfficeSystem(menu_code=menu_code, input_date=date_ref)
        bos.recursive_download_dataset()
    
    insert_every_menu_data()

    activator.on_mos()
    MOS_MENU_CODES_FOR_SNAPSHOT = ['2205', '2160', '2820']
    for menu_code in tqdm(MOS_MENU_CODES_FOR_SNAPSHOT):
        download_all_snapshot_datasets_of_timeseries(end_date=date_ref, menu_code=menu_code)
    mos5105 = OfficeSystem(menu_code='5105', fund_code='000005')
    mos5105.recursive_download_dataset()

    fetcher_2160 = Menu2160Snapshots()
    fetcher_2160.fetch_snapshots()
    fetcher_2160.insert_all()
    
    fetcher_2205 = Menu2205Snapshots()
    fetcher_2205.fetch_snapshots()
    fetcher_2205.insert_all()


    for menu_code, _ in MAPPING_PSEUDO_CODES.items():
        mos = MOS1100(menu_code=menu_code, start_date=date_ref, end_date=date_ref)
        mos.recursive_download_dataset()
        wait_for_n_seconds(1)

    file_names_local = scan_files_including_regex(file_folder='C:/datalake/dataset-menu1100', regex=f'menu1100-.*-at{date_ref.replace("-","")}')
    for file_name in tqdm(file_names_local):
        upload_files_to_s3(file_folder_local=DATALAKE_DIR, regex=file_name, bucket='dataset-system', bucket_prefix='dataset-menu1100')

    for ticker_pseudo in MAPPING_PSEUDO_CODES.values():
        insert_menu1100(ticker_pseudo, date_ref=date_ref)

    download_menu2205s_non_priority(date_ref=date_ref)
    download_menu2205s_all(date_ref=date_ref)
    dates_and_codes = get_nonexisting_pairs_date_code_for_menu2205()
    for date, code in tqdm(dates_and_codes):
        if date == date_ref:
            menu2205_fetcher = Menu2205(fund_code=code, date_ref=date)
            menu2205_fetcher.fetch_unit_df()
            menu2205_fetcher.insert_unit()

    m = MOS2206(date_ref=date_ref)
    m.recursive_download_dataset()
    menu2206_fetcher = Menu2206s()
    menu2206_fetcher.fetch_snapshots()
    menu2206_fetcher.insert_all()

    return None

def run_download_tasks_recursively():
    try:
        run_download_tasks()
    except Exception as e:
        wait_for_n_seconds(60)
        run_download_tasks()
    return None



def print_remaining_time():
    next_run = schedule.next_run()
    if next_run:
        now = datetime.now()
        remaining_time = next_run - now

        # 남은 시간이 0 이하일 경우, 다음 실행을 건너뜁니다.
        if remaining_time.total_seconds() <= 0:
            print("(No valid next task time found)")
            return

        days = remaining_time.days
        hours, remainder = divmod(remaining_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        # 현재 시간을 영어 형식으로 출력하고 남은 시간 출력
        current_time = now.strftime("(%Y-%m-%d %H:%M)")
        
        if days > 0:
            print(f"{current_time} Next task will run in {days} days, {int(hours)} hours and {int(minutes)} minutes")
        else:
            print(f"{current_time} Next task will run in {int(hours)} hours and {int(minutes)} minutes")

def main(enforce):
    # 매일 05:00에 다운로드 작업 예약
    schedule.every().day.at("03:00").do(run_download_tasks_recursively)

    # 10분마다 남은 시간 출력
    schedule.every(10).minutes.do(print_remaining_time)

    # 강제 즉시 실행 옵션 처리
    if enforce:
        print("Enforce option provided, running download tasks immediately.")
        run_download_tasks()

    # 스케줄 실행 대기 루프
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    # 명령줄 인자 파싱
    parser = argparse.ArgumentParser(description="Schedule download tasks with optional enforcement.")
    parser.add_argument('--enforce', action='store_true', help="Run tasks immediately instead of waiting for the scheduled time.")
    args = parser.parse_args()

    # main 함수 호출, enforce 옵션 처리
    main(args.enforce)
