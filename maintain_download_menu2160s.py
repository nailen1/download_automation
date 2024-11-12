from download_automation import download_all_timeseries_datasets, Activator

activator = Activator()
activator.on_mos()

download_all_timeseries_datasets(menu_code='2160')