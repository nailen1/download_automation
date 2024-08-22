# maintain_download_all_datasets.py

from download_automation import download_all_datasets_of_snapshot, download_all_snapshot_datasets_of_timeseries

def main():
    download_all_snapshot_datasets_of_timeseries(menu_code='8186')

if __name__ == "__main__":
    main()