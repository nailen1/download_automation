from download_automation import *
from database_managing import insert_every_menu_data
from datetime import datetime

activator = Activator()
activator.on_mos()

dates = get_dates_to_download_for_menu2110()
for date in dates:
    current_hour = datetime.now().hour
    if 2 <= current_hour < 6:
        print(f"Current time is {current_hour}:00 (past 2 AM). Stopping the loop.")        
        break
    print(f"# Downloading data for date: {date}")
    mos = OfficeSystem(menu_code='2110', input_date=date)
    mos.recursive_download_dataset()
    insert_every_menu_data()

dates = get_dates_to_download_for_menu3412()
for date in dates:
    current_hour = datetime.now().hour
    if 2 <= current_hour < 6:
        print(f"Current time is {current_hour}:00 (past 2 AM). Stopping the loop.")        
        break
    print(f"# Downloading data for date: {date}")
    mos = OfficeSystem(menu_code='3412', input_date=date)
    mos.recursive_download_dataset()
    insert_every_menu_data()

activator.on_bos()

dates = get_dates_to_download_for_menu3233()

for date in dates:
    current_hour = datetime.now().hour
    if 2 <= current_hour < 6:
        print(f"Current time is {current_hour}:00 (past 2 AM). Stopping the loop.")        
        break
    print(f"# Downloading data for date: {date}")
    bos = OfficeSystem(menu_code='3233', input_date=date)
    bos.recursive_download_dataset()
    insert_every_menu_data()

dates = get_dates_to_download_for_menu3421()
for date in dates:
    current_hour = datetime.now().hour
    if 2 <= current_hour < 6:
        print(f"Current time is {current_hour}:00 (past 2 AM). Stopping the loop.")        
        break
    print(f"# Downloading data for date: {date}")
    bos = OfficeSystem(menu_code='3421', input_date=date)
    bos.recursive_download_dataset()
    insert_every_menu_data()