from download_automation import download_every_timeseries_dataset_of_fund, Activator
from shining_pebbles import get_yesterday

activator = Activator()
activator.on_mos()

download_every_timeseries_dataset_of_fund(menu_code='2160')