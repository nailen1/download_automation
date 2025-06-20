from functools import partial
from shining_pebbles import get_date_range, get_yesterday
from download_automation import DATE_GENESIS_REAL
from mongodb_controller import (
    COLLECTION_2110,
    COLLECTION_3412,
    COLLECTION_3421,
    COLLECTION_3233
)

def get_dates_to_download_in_collection_menu(collection_menu):
    dates = get_date_range(start_date_str=DATE_GENESIS_REAL, end_date_str=get_yesterday())
    dates_in_db = collection_menu.distinct('date_ref')
    dates_to_download = sorted(list(set(dates) - set(dates_in_db)))
    return dates_to_download

get_dates_to_download_for_menu2110 = partial(get_dates_to_download_in_collection_menu, COLLECTION_2110)
get_dates_to_download_for_menu3412 = partial(get_dates_to_download_in_collection_menu, COLLECTION_3412)
get_dates_to_download_for_menu3421 = partial(get_dates_to_download_in_collection_menu, COLLECTION_3421)
get_dates_to_download_for_menu3233 = partial(get_dates_to_download_in_collection_menu, COLLECTION_3233)
