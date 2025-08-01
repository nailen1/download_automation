from shining_pebbles import *
import csv 
from tqdm import tqdm
from .constants import *
from .office_system import *
from .date_utils import *
from .existings_picker import *
from fund_insight_engine.fund_data_retriever.fund_mappings import (
    get_mapping_fund_names_with_priority_1, 
    get_mapping_fund_names_with_priority_2, 
    get_mapping_fund_names_with_non_priority,
    get_mapping_fund_names_mongodb
)


def get_all_fund_codes():
    df_fundlist = get_df_fundlist_from_menu2160_snapshots_in_s3()    
    fund_codes = df_fundlist.index.tolist()
    return fund_codes

FUND_CODES_ALL = get_all_fund_codes()


def get_input_dates_downloaded_in_file_folder(menu_code, file_folder=None, form='%Y%m%d'):
    file_folder = os.path.join(BASE_FOLDER_PATH, f'dataset-menu{menu_code}') if file_folder is None else file_folder
    file_names_downloaded = scan_files_including_regex(file_folder=file_folder, regex=f'menu{menu_code}')
    input_dates_downloaded = [pick_input_date_in_file_name(file_name) for file_name in file_names_downloaded]
    if form == '%Y-%m-%d':
        input_dates_downloaded = [f'{date[:4]}-{date[4:6]}-{date[6:8]}' for date in input_dates_downloaded]
    return input_dates_downloaded


def download_all_snapshot_datasets_of_timeseries(menu_code, start_date=DATE_GENESIS_REAL, end_date=get_yesterday()):
    print(f'- download all snapshot datasets: menu{menu_code}')
    dates = get_date_range(start_date_str=start_date, end_date_str=end_date)
    dates_downloaded = get_input_dates_downloaded_in_file_folder(menu_code, file_folder=os.path.join(BASE_FOLDER_PATH, f'dataset-menu{menu_code}-snapshot'), form='%Y-%m-%d')
    if dates_downloaded != []:
        print(f'{len(dates_downloaded)}/{len(dates)} dates downloaded: ... {dates_downloaded[-1]}')
        dates = sorted(list(set(dates) - set(dates_downloaded)))
    dates = sorted(dates, reverse=True)
    for date in tqdm(dates):
        print(f' ▶ input date: {date}')
        mos = OfficeSystem(menu_code=menu_code, input_date=date)
        mos.recursive_download_dataset()
    return None


def get_fund_codes_downloaded_in_file_folder(menu_code, input_date=None, end_date=None, file_folder=None):
    file_folder = os.path.join(BASE_FOLDER_PATH, f'dataset-menu{menu_code}') if file_folder is None else file_folder
    if input_date and not end_date:
        regex = f'menu{menu_code}.*-at{input_date.replace("-","")}-.*.csv$'
    elif not input_date and end_date:
        regex = f'menu{menu_code}.*-to{end_date.replace("-","")}-.*.csv$'
    file_names_downloaded = scan_files_including_regex(file_folder=file_folder, regex=regex)
    fund_codes_downloaded = [pick_code_in_file_name(file_name) for file_name in file_names_downloaded]
    return fund_codes_downloaded



def save_download_log_of_timeseries_datasets(file_folder, end_date):
    menu_code = file_folder.split('menu')[1][:4]
    file_folder_path = os.path.join(BASE_FOLDER_PATH, file_folder)
    print(f'- check download datasets in folder: {file_folder_path}')
    file_names = scan_files_including_regex(file_folder=file_folder_path, regex=f'^menu.*-to{end_date.replace("-","")}-save.*.csv$')
    bucket = []
    for file_name in file_names:
        fund_code = file_name.split('-code')[1].split('-')[0]
        try:
            start_date = file_name.split('from')[1][:8]
        except:
            start_date = np.nan
        end_date = file_name.split('-to')[1][:8]
        save_date = file_name.split('-save')[1][:8]

        try:
            df = open_df_in_file_folder_by_regex(file_folder=file_folder_path, regex=file_name)
            dates_in_df = df.index.dropna()
            n_days = len(dates_in_df)
            if n_days == 0:
                t_i = np.nan
                t_f = np.nan
            else:
                t_i = dates_in_df[0]
                t_f = dates_in_df[-1]
        except:
            t_i = np.nan
            t_f = np.nan    

        dct = {
            'menu_code': menu_code,
            'fund_code': fund_code,
            'start_date': start_date,
            'end_date': end_date,
            'file_name': file_name,
            'n_days': n_days,
            't_i': t_i,
            't_f': t_f,
            'save_date': save_date
        }
        bucket.append(dct)
    df = pd.DataFrame(bucket)
    # df['fund_code'] = df['fund_code'].astype(str).apply(lambda x: x.zfill(6) if len(x) <= 6 else x)
    df['fund_code'] = df['fund_code'].astype(str).apply(lambda x: f'{x.zfill(6)}' if len(x) <= 6 else x)
    file_folder_log = os.path.join(BASE_FOLDER_PATH, 'dataset-log')
    check_folder_and_create_folder(file_folder_log)
    file_name = f'log-{file_folder}-to{end_date.replace("-","")}-save{get_today("%Y%m%d%H")}.csv'
    file_path = os.path.join(file_folder_log, file_name)
    df.to_csv(file_path, quoting=csv.QUOTE_NONNUMERIC)
    print(f'- save log to: {file_path}')
    return df


def save_download_log_of_sanpshot_datasets(file_folder, input_date):
    menu_code = file_folder.split('menu')[1][:4]
    file_folder_path = os.path.join(BASE_FOLDER_PATH, file_folder)
    print(f'- check download datasets in folder: {file_folder_path}')
    file_names = scan_files_including_regex(file_folder=file_folder_path, regex=f'^menu.*-at{input_date.replace("-","")}-.*.csv$')
    bucket = []
    for file_name in file_names:
        fund_code = file_name.split('-code')[1].split('-')[0]
        input_date = file_name.split('-at')[1][:8]
        save_date = file_name.split('-save')[1][:8]
        try:
            df = open_df_in_file_folder_by_regex(file_folder=file_folder_path, regex=file_name)
            rows_in_df = df.index.dropna()
            n_rows = len(rows_in_df)
            if n_rows == 0:
                n_rows = np.nan
        except:
            n_rows = np.nan 
        dct = {
            'menu_code': menu_code,
            'fund_code': fund_code,
            'input_date': input_date,
            'file_name': file_name,
            'n_rows': n_rows,
            'save_date': save_date
        }
        bucket.append(dct)
    df = pd.DataFrame(bucket)
    df['fund_code'] = df['fund_code'].astype(str).apply(lambda x: f'{x.zfill(6)}' if len(x) <= 6 else x)
    file_folder_log = os.path.join(BASE_FOLDER_PATH, 'dataset-log')
    check_folder_and_create_folder(file_folder_log)
    file_name = f'log-{file_folder}-at{input_date.replace("-","")}-save{get_today("%Y%m%d%H")}.csv'
    file_path = os.path.join(file_folder_log, file_name)
    df.to_csv(file_path, quoting=csv.QUOTE_NONNUMERIC)
    print(f'- save log to: {file_path}')
    return df


def check_download_folders_in_root(folder_regex):
    print(f'- check download folders in root folder: {os.path.join(BASE_FOLDER_PATH, folder_regex)}')
    folders = scan_files_including_regex(file_folder=BASE_FOLDER_PATH, regex=folder_regex, option='name')
    for folder in folders:
        print(folder)
        save_download_log_of_timeseries_datasets(folder)
    return None


def download_all_snapshot_datasets(menu_code='2205', input_date=None, fund_codes=None, category='all'):
    input_date = input_date or get_date_n_days_ago(get_today("%Y%m%d"),1)

    df_fundlist = get_df_fundlist_from_menu2160_snapshots_in_s3(category=category)    

    for fund_code in tqdm(FUND_CODES_PRIORITEZED):
        mos = OfficeSystem(menu_code=menu_code, fund_code=fund_code, input_date=input_date)
        mos.recursive_download_dataset()

    for fund_code in tqdm(FUND_CODES_MENU2205_PRIORITY):
        mos = OfficeSystem(menu_code=menu_code, fund_code=fund_code, input_date=input_date)
        mos.recursive_download_dataset()

    fund_codes = df_fundlist.index.tolist()
    fund_codes_downloaded = get_fund_codes_downloaded_in_file_folder(menu_code=menu_code, input_date=input_date)
    if fund_codes_downloaded != []:
        print(f'{len(fund_codes_downloaded)}/{len(fund_codes)} funds downloaded: ... {fund_codes_downloaded[-1]}')
        fund_codes = list(set(fund_codes) - set(fund_codes_downloaded))
    fund_codes = sorted(fund_codes)
    for fund_code in tqdm(fund_codes):
        mos = OfficeSystem(menu_code=menu_code, fund_code=fund_code, input_date=input_date)
        mos.recursive_download_dataset()

    save_download_log_of_sanpshot_datasets(file_folder=f'dataset-menu{menu_code}', input_date=input_date)
    return None


def download_all_period_datasets(menu_code='8870', date_pairs=None):
    date_pairs_nonexistent = pick_nonexistent_date_pairs_in_period_datasets(menu_code='8870', date_pairs=DATE_PAIRS_DEFAULT)
    date_pairs = date_pairs or date_pairs_nonexistent

    for date_pair in tqdm(date_pairs):
        start_date, end_date = date_pair
        mos = OfficeSystem(menu_code=menu_code, start_date=start_date, end_date=end_date)
        mos.recursive_download_dataset()
    return None


def download_all_timeseries_datasets(menu_code='2160', fund_codes=None, start_date=None, end_date=None, category='all'):
    start_date = start_date or DATE_GENESIS
    end_date = end_date or get_yesterday()
    fund_codes_all = get_mapping_fund_names_mongodb().keys()
    fund_codes_existing = get_fund_codes_downloaded_in_file_folder(menu_code=menu_code, end_date=end_date)
    fund_codes = fund_codes or list(set(fund_codes_all) - set(fund_codes_existing))
    for fund_code in tqdm(fund_codes):
        mos = OfficeSystem(menu_code=menu_code, fund_code=fund_code, start_date=start_date, end_date=end_date)
        mos.recursive_download_dataset()

    save_download_log_of_timeseries_datasets(file_folder=f'dataset-menu{menu_code}', end_date=end_date)
    return None

def download_menu2205s_priority_1(date_ref=None):
    menu_code = '2205'
    date_ref = date_ref or get_yesterday()
    fund_codes_priority_1 = list(get_mapping_fund_names_with_priority_1().keys())
    for fund_code in tqdm(fund_codes_priority_1):
        mos = OfficeSystem(menu_code=menu_code, fund_code=fund_code, input_date=date_ref)
        mos.recursive_download_dataset()
    save_download_log_of_sanpshot_datasets(file_folder=f'dataset-menu{menu_code}', input_date=date_ref)
    return None

def download_menu2205s_priority_2(date_ref=None):
    menu_code = '2205'
    date_ref = date_ref or get_yesterday()
    fund_codes_priority_2 = list(get_mapping_fund_names_with_priority_2().keys())
    for fund_code in tqdm(fund_codes_priority_2):
        mos = OfficeSystem(menu_code=menu_code, fund_code=fund_code, input_date=date_ref)
        mos.recursive_download_dataset()
    save_download_log_of_sanpshot_datasets(file_folder=f'dataset-menu{menu_code}', input_date=date_ref)
    return None

def download_menu2205s_non_priority(date_ref=None):
    menu_code = '2205'
    date_ref = date_ref or get_yesterday()
    fund_codes_non_priority = list(get_mapping_fund_names_with_non_priority().keys())
    for fund_code in tqdm(fund_codes_non_priority):
        mos = OfficeSystem(menu_code=menu_code, fund_code=fund_code, input_date=date_ref)
        mos.recursive_download_dataset()
    save_download_log_of_sanpshot_datasets(file_folder=f'dataset-menu{menu_code}', input_date=date_ref)
    return None

def download_menu2205s_all(date_ref=None):
    menu_code = '2205'
    date_ref = date_ref or get_yesterday()
    fund_codes_all = list(get_mapping_fund_names_mongodb().keys())
    for fund_code in tqdm(fund_codes_all):
        mos = OfficeSystem(menu_code=menu_code, fund_code=fund_code, input_date=date_ref)
        mos.recursive_download_dataset()
    save_download_log_of_sanpshot_datasets(file_folder=f'dataset-menu{menu_code}', input_date=date_ref)
    return None
