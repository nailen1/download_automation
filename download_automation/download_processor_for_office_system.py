# download_processor_for_office_system.py
# version20240808 refactioing

# External libraries
from shining_pebbles import *
from aws_s3_controller import *

# Internal modules
from .screen_control_utils import *
from .coordinate_tracer import *
from .constants import *
from .download_processor_for_excel import is_on_running_excel


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
        move_to_image(IMAGE_PATH_SAVE_FORMAT_CONFIRM_BUTTON)
        wait_for_n_seconds(1)
        click()
        return False
    elif is_on_running_excel():
        print('|- exception: excel is already running.')
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
        elif attempt >= max_retries:
            print('|- max retries reached. data loading did not complete.')
            return False
        elif is_on_running_excel():
            print('|- exception: excel is already running.')
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
    elif is_on_running_excel():
        print('|- exception: excel is already running.')
        return False
    else:
        return is_there_data_length_caution_popup_on_data_loading(max_retries, attempt + 1)
    
def is_there_no_data_popup(max_retries=5, attempt=1, max_check_time=3):
    print(f'|- checking no data popup ... (attempt {attempt})')
    wait_for_n_seconds(1)
    caution = check_image_appearance(IMAGE_PATH_NO_DATA_POPUP, max_check_time=max_check_time)
    if caution:
        print('|- no data popup appeared.')
        return True
    elif attempt >= max_retries:
        print('|- max retries reached. no data popup found.')
        return False
    else:
        return is_there_no_data_popup(max_retries, attempt + 1)
    

    
def is_loading_started(enforce=False):
    return wait_until_image_appears(image_path=IMAGE_PATH_LOADING_SEARCH_GO, enforce=enforce)

def is_loading_completed(enforce=False):
    return wait_until_image_disappears(image_path=IMAGE_PATH_LOADING_SEARCH_GO, enforce=enforce)

def is_on_login_window(enforce=False):
    return wait_until_image_appears(image_path=IMAGE_PATH_HEADER_LOGIN, enforce=enforce)

def is_there_mos_exception_popup(enforce=False):
    return wait_until_image_appears(image_path=IMAGE_PATH_MOS_EXCEPTION_POPUP, enforce=enforce)
    
def check_system_is_running(name_system, enforce=False):
    mapping_name_to_image = {
        'MOS': IMAGE_PATH_ICON_MOS,
        'BOS': IMAGE_PATH_ICON_BOS,
    }
    if wait_until_image_appears(image_path=mapping_name_to_image[name_system], enforce=enforce):
        print(f'|- ({name_system}) is running ... ')
        return True
    else:
        print(f'|- ({name_system}) is not running ... ')
        return False
