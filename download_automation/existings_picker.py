from shining_pebbles import *
from .constants import BASE_FOLDER_PATH, DATE_GENESIS_REAL, FUND_CODES_PRIORITEZED
from .date_utils import *
from .download_processor_for_s3 import get_df_fundlist_from_menu2160_snapshots_in_s3
import os
import re

def get_file_names_of_period_datasets(menu_code, date_pairs, save_date=None, file_folder=None):
    file_folder = os.path.join(BASE_FOLDER_PATH, f'dataset-menu{menu_code}') if file_folder is None else file_folder
    if save_date:
        regex = f'menu{menu_code}.*-between{date_pairs[0].replace("-","")}-and{date_pairs[1].replace("-","")}-save{save_date.replace("-", "")}.csv$'
    else:
        regex = f'menu{menu_code}.*-between{date_pairs[0].replace("-","")}-and{date_pairs[1].replace("-","")}-save{get_today().replace("-", "")[:6]}.*$'
    file_names_downloaded = scan_files_including_regex(file_folder=file_folder, regex=regex)
    return file_names_downloaded


def pick_date_pair_infile_name_period(text):
    pattern = r"-between(\d{8})-and(\d{8})"
    match = re.search(pattern, text)
    if match:
        return (match.group(1), match.group(2))
    return None


def pick_existing_date_pairs_in_period_datasets(menu_code, date_pairs):
    existing_date_pairs = []
    for date_pair in date_pairs:
        file_names = get_file_names_of_period_datasets(menu_code=menu_code, date_pairs=date_pair)
        if file_names:
            existing_date_pair = pick_date_pair_infile_name_period(file_names[-1])
            existing_date_pairs.append(existing_date_pair)
    return existing_date_pairs


def exclude_existing_date_pairs(date_pairs, existing_date_pairs):
    date_pairs_formatted = [(start_date.replace("-", ""), end_date.replace("-", "")) for start_date, end_date in date_pairs]
    date_pairs_nonexistent = list(set(date_pairs_formatted) - set(existing_date_pairs))
    return date_pairs_nonexistent


def pick_nonexistent_date_pairs_in_period_datasets(menu_code, date_pairs):
    existing_date_pairs = pick_existing_date_pairs_in_period_datasets(menu_code=menu_code, date_pairs=date_pairs)
    date_pairs_nonexistent = exclude_existing_date_pairs(date_pairs, existing_date_pairs)
    return date_pairs_nonexistent


DATE_PAIRS_DEFAULT = get_date_pairs_of_months(start_date=DATE_GENESIS_REAL, end_date=get_yesterday())




def get_file_names_of_timeseries_datasets(menu_code, date_pairs, save_date=None, file_folder=None):
    file_folder = os.path.join(BASE_FOLDER_PATH, f'dataset-menu{menu_code}') if file_folder is None else file_folder
    if save_date:
        regex = f'menu{menu_code}.*-from{date_pairs[0].replace("-","")}-to{date_pairs[1].replace("-","")}-save{save_date.replace("-", "")}.csv$'
    else:
        regex = f'menu{menu_code}.*-from{date_pairs[0].replace("-","")}-to{date_pairs[1].replace("-","")}-save{get_today().replace("-", "")[:6]}.*$'
    file_names_downloaded = scan_files_including_regex(file_folder=file_folder, regex=regex)
    return file_names_downloaded


def pick_fund_code_in_file_name_timeseries(text):
    pattern = r"-code(\w{6})"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None


def pick_fund_codes_in_period_datasets(menu_code, date_pairs):
    existing_fund_codes = []
    for date_pair in date_pairs:
        file_names = get_file_names_of_timeseries_datasets(menu_code=menu_code, date_pairs=date_pair)
        if file_names:
            existing_fund_code = pick_fund_code_in_file_name_timeseries(file_names[-1])
            existing_fund_codes.append(existing_fund_code)
    return existing_fund_codes


def exclude_existing_elements(elements, existing_elements):
    elements_nonexistent = list(set(elements) - set(existing_elements))
    return elements_nonexistent


def pick_nonexistent_fund_codes_in_timeseries_datasets(menu_code, date_pairs, category='all'):
    df_fundlist = get_df_fundlist_from_menu2160_snapshots_in_s3(category=category)    
    fund_codes = df_fundlist.index.tolist()
    existing_fund_codes = pick_fund_codes_in_period_datasets(menu_code=menu_code, date_pairs=date_pairs)
    fund_codes_nonexistent = exclude_existing_elements(fund_codes, existing_fund_codes)
    fund_codes_ordered = FUND_CODES_PRIORITEZED + exclude_existing_elements(fund_codes_nonexistent, FUND_CODES_PRIORITEZED)
    return fund_codes_ordered

