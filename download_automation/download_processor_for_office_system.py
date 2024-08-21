# download_processor_for_office_system.py
# version20240808 refactioing

# External libraries
from shining_pebbles import *
from aws_s3_controller import *

# Internal modules
from screen_control_utils import *
from coordinate_tracer import *
from constants import *


def is_now_search_loading(max_retries=20, attempt=1):
    print(f'|- search loading ... (attempt {attempt})')
    wait_for_n_seconds(1)
    loading = check_image_appearance(IMAGE_PATH_LOADING_SEARCH_GO, max_check_time=5)
    if loading:
        if attempt >= max_retries:
            print('|- max retries reached. search loading did not complete.')
            return False
        return is_now_search_loading(max_retries, attempt + 1)
    else:
        print('|- search loaded.')
        return False

def is_data_loading_started(max_retries=20, attempt=1, max_check_time=10):
    print(f'|- waiting for data loading to start (attempt {attempt})')
    loading = check_image_appearance(IMAGE_PATH_LOADING_EXCEL_GO, max_check_time=max_check_time)
    if loading:
        print('|- data loading started.')
        return True
    elif attempt >= max_retries:
        print('|- max retries reached. data loading did not start.')
        return False
    else:
        return is_data_loading_started(max_retries, attempt + 1)

def is_now_data_loading(max_retries=20, attempt=1, max_check_time=5):
    print(f'|- data loading ... (attempt {attempt})')
    loading = check_image_appearance(IMAGE_PATH_LOADING_EXCEL_GO, max_check_time=max_check_time)
    if loading:
        if is_there_data_length_caution_popup_on_data_loading():
            wait_for_n_seconds(2)
            move_to_image(IMAGE_PATH_EXCEL_CAUTION_CONFIRM_BUTTON)
            wait_for_n_seconds(1)
            click()
        if attempt >= max_retries:
            print('|- max retries reached. data loading did not complete.')
            return False
        return is_now_data_loading(max_retries, attempt + 1)
    else:
        print('|- data loaded.')
        return False

def is_there_data_length_caution_popup_on_data_loading(max_retries=5, attempt=1, max_check_time=3):
    print(f'|- checking data length caution popup ... (attempt {attempt})')
    wait_for_n_seconds(1)
    caution = check_image_appearance(IMAGE_PATH_DATA_LENGTH_CAUTION_POPUP, max_check_time=max_check_time)
    if caution:
        print('|- data length caution popup appeared.')
        return True
    elif attempt >= max_retries:
        print('|- max retries reached. no data length caution popup found.')
        return False
    else:
        return is_there_data_length_caution_popup_on_data_loading(max_retries, attempt + 1)