from pyautogui import click
from menu_downloader.screen_controller.screen_basis import (
    wait_for_n_seconds,
    wait_until_image_appears,
    wait_until_image_disappears,
    is_image_on_screen,
    move_to_image,
)
from menu_downloader.screen_controller.screen_utils import (
    click_button
)
from menu_downloader.excel_controller.excel_utils import (
    is_on_excel_window
)
from menu_downloader.screen_controller.screen_time_consts import (
    TIME_INTERVAL_BETWEEN_CLICK_AND_KEYBOARD_CONTOL,
)
from menu_downloader.menu_controller.menu_path_director import (
    IMAGE_PATH_BAR_LOADING_IDENTIFIER,
    IMAGE_PATH_DATA_LENGTH_POPUP_IDENTIFIER,
    IMAGE_PATH_LOADING_EXCEL_GO,
    IMAGE_PATH_DATA_LENGTH_CAUTION_POPUP,
    IMAGE_PATH_EXCEL_CAUTION_CONFIRM_BUTTON,
    IMAGE_PATH_SAVE_FORMAT_CONFIRM_BUTTON,
)
from menu_downloader.excel_controller import (
    is_on_excel_window
)
from .menu_time_consts import TIME_INTERVAL_BETWEEN_PRESSING_LOAD_BUTTON_AND_LOADING

def is_bar_loading():
    return is_image_on_screen(image_path=IMAGE_PATH_BAR_LOADING_IDENTIFIER, option_verbose=False)

def is_data_length_popup():
    return is_image_on_screen(image_path=IMAGE_PATH_BAR_LOADING_IDENTIFIER, option_verbose=False)

def is_data_length_popup():
    return is_image_on_screen(image_path=IMAGE_PATH_DATA_LENGTH_POPUP_IDENTIFIER, option_verbose=False)

def wait_until_bar_loading_appears(timeout=30, check_interval=1, option_verbose=False):
    return wait_until_image_appears(image_path=IMAGE_PATH_BAR_LOADING_IDENTIFIER, timeout=timeout, check_interval=check_interval, option_verbose=option_verbose)

def wait_until_bar_loading_disappears(timeout=30, check_interval=1, option_verbose=False):
    return wait_until_image_disappears(image_path=IMAGE_PATH_BAR_LOADING_IDENTIFIER, timeout=timeout, check_interval=check_interval, option_verbose=option_verbose)

def is_now_bar_loading(max_retries=30, attempt=1, timeout=5, check_interval=1):
    print(f'|- data loading ... (attempt {attempt})')
    wait_for_n_seconds(TIME_INTERVAL_BETWEEN_PRESSING_LOAD_BUTTON_AND_LOADING)
    if not is_bar_loading():
        print(f'|- assume data loaded instantly, i.e. within {TIME_INTERVAL_BETWEEN_PRESSING_LOAD_BUTTON_AND_LOADING}s.')
        return False
    loaded = wait_until_bar_loading_disappears(timeout=timeout, check_interval=check_interval)
    if loaded:
        print('|- data loaded.')
        return False
    else:
        if is_data_length_popup():
           wait_for_n_seconds(TIME_INTERVAL_BETWEEN_CLICK_AND_KEYBOARD_CONTOL)
           click_button(IMAGE_PATH_DATA_LENGTH_POPUP_IDENTIFIER)
        if attempt >= max_retries:
            print('|- max retries reached. data loading did not complete.')
            return False
        elif is_on_excel_window():
            print('|- exception: excel is already running.')
            return False
        return is_now_bar_loading(max_retries, attempt + 1)


def is_now_data_loading(max_retries=20, attempt=1, max_check_time=5):
    print(f'|- data loading ... (attempt {attempt})')
    loading = wait_until_image_appears(image_path=IMAGE_PATH_LOADING_EXCEL_GO, timeout=max_check_time)
    if loading:
        if is_there_data_length_caution_popup_on_data_loading():
            wait_for_n_seconds(2)
            move_to_image(IMAGE_PATH_EXCEL_CAUTION_CONFIRM_BUTTON)
            wait_for_n_seconds(1)
            click()
        elif attempt >= max_retries:
            print('|- max retries reached. data loading did not complete.')
            return False
        elif is_on_excel_window():
            print('|- exception: excel is already running.')
            return False
        return is_now_data_loading(max_retries, attempt + 1)
    else:
        print('|- data loaded.')
        return False

def is_there_data_length_caution_popup_on_data_loading(max_retries=5, attempt=1, max_check_time=3):
    print(f'|- checking data length caution popup ... (attempt {attempt})')
    wait_for_n_seconds(1)
    caution = wait_until_image_appears(IMAGE_PATH_DATA_LENGTH_CAUTION_POPUP, timeout=max_check_time)
    if caution:
        print('|- data length caution popup appeared.')
        return True
    elif attempt >= max_retries:
        print('|- max retries reached. no data length caution popup found.')
        return False
    elif is_on_excel_window():
        print('|- exception: excel is already running.')
        return False
    else:
        return is_there_data_length_caution_popup_on_data_loading(max_retries, attempt + 1)
    

def is_data_loading_started(max_retries=20, attempt=1, max_check_time=10):
    print(f'|- waiting for data loading to start (attempt {attempt})')
    loading = wait_until_image_appears(IMAGE_PATH_LOADING_EXCEL_GO, timeout=max_check_time)
    if loading:
        print('|- data loading started.')
        return True
    elif attempt >= max_retries:
        print('|- max retries reached. data loading did not start.')
        move_to_image(IMAGE_PATH_SAVE_FORMAT_CONFIRM_BUTTON)
        wait_for_n_seconds(1)
        click()
        return False
    elif is_on_excel_window():
        print('|- exception: excel is already running.')
        return False
    else:
        return is_data_loading_started(max_retries, attempt + 1)
    
# def is_now_data_loading(max_retries=20, attempt=1, max_check_time=5):
#     print(f'|- data loading ... (attempt {attempt})')
#     loading = check_image_appearance(IMAGE_PATH_LOADING_EXCEL_GO, max_check_time=max_check_time)
#     if loading:
#         if is_there_data_length_caution_popup_on_data_loading():
#             wait_for_n_seconds(2)
#             move_to_image(IMAGE_PATH_EXCEL_CAUTION_CONFIRM_BUTTON)
#             wait_for_n_seconds(1)
#             click()
#         elif attempt >= max_retries:
#             print('|- max retries reached. data loading did not complete.')
#             return False
#         elif is_on_running_excel():
#             print('|- exception: excel is already running.')
#             return False
#         return is_now_data_loading(max_retries, attempt + 1)
#     else:
#         print('|- data loaded.')
#         return False



# def is_on_running_excel():
#     print('| (step) checking excel is running ...')
#     wait_for_n_seconds(1)
#     caution = check_image_appearance(IMAGE_PATH_EXCEL_HEADER, max_check_time=3)
#     if caution:
#         print('|- excel is running.')
#         return True
#     else:
#         print('|- excel is not running.')
#         return False