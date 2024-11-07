import schedule
import time
from datetime import datetime, timedelta
import argparse
from download_automation import *

def run_download_tasks():
    activator = Activator()
    
    activator.on_mos()
    download_all_snapshot_datasets_of_timeseries(end_date=get_yesterday(), menu_code='2160')
    download_all_snapshot_datasets_of_timeseries(end_date=get_yesterday(), menu_code='2820')
    download_all_snapshot_datasets(input_date=get_yesterday(), menu_code='2205')
    download_all_snapshot_datasets_of_timeseries(menu_code='2205')
    input_date = get_yesterday()
    mos_menu_codes = ['3412', '2110']
    for menu_code in tqdm(mos_menu_codes):
        mos = OfficeSystem(menu_code=menu_code, input_date=input_date)
        mos.recursive_download_dataset()

    activator.on_bos()
    input_date = get_yesterday()
    bos_menu_codes = ['8186', '3421', '3233']
    for menu_code in tqdm(bos_menu_codes):
        bos = OfficeSystem(menu_code=menu_code, input_date=input_date)
        bos.recursive_download_dataset()
    download_all_snapshot_datasets_of_timeseries(end_date=get_yesterday(), menu_code='8186')

    # 매주 토요일에 추가 작업 실행
    # if datetime.today().weekday() == 5:  # 토요일 (0: 월요일, 5: 토요일)
    #     activator.on_mos()
    #     download_every_timeseries_dataset_of_fund(menu_code='2160')

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
    schedule.every().day.at("05:00").do(run_download_tasks)

    # 매주 토요일 05:00에 추가 작업도 포함한 다운로드 작업 예약
    schedule.every().saturday.at("05:00").do(run_download_tasks)

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
