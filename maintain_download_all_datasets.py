# maintain_download_all_datasets.py
from shining_pebbles import get_today, get_yesterday
from download_automation import *
from tqdm import tqdm

def main():
    activator = Activator()
    activator.on_mos()

    download_all_snapshot_datasets_of_timeseries(end_date=get_yesterday(),  menu_code='2160')
    download_all_snapshot_datasets_of_timeseries(end_date=get_yesterday(), menu_code='2820')
    download_every_snapshot_dataset_of_fund(input_date=get_yesterday(), menu_code='2205')
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

    activator.on_mos()
    download_every_timeseries_dataset_of_fund(menu_code='2160')


if __name__ == "__main__":
    main()