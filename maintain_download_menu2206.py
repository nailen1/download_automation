from download_automation import Activator
from menu_downloader import MOS2206
from shining_pebbles import get_date_range

activator = Activator()
activator.on_mos()

activator.on_mos()
dates = get_date_range(start_date_str='2025-04-03', end_date_str='2025-04-13')
for date in dates:
    mos = MOS2206(date_ref=date)
    mos.execute_all_sequences()