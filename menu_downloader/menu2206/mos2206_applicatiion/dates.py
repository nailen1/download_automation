from mongodb_controller import COLLECTION_2206
from shining_pebbles import extract_dates_ref_in_file_folder_by_regex, get_date_range, get_yesterday

def get_dates_to_download_for_menu2206(option_force_delete=False):
    dates = get_date_range(start_date_str='2024-01-01', end_date_str=get_yesterday())
    dates_db = sorted(COLLECTION_2206.distinct('일자'), reverse=True)
    # dates_local = sorted(extract_dates_ref_in_file_folder_by_regex(file_folder='C:/datalake/dataset-menu2206', regex='menu2206-code000000-at'), reverse=True)
    dates_to_download = sorted(set(dates) - set(dates_db), reverse=True)
    return dates_to_download