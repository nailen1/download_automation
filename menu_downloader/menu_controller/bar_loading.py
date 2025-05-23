from menu_downloader.screen_controller.screen_basis import (
    wait_for_n_seconds,
    wait_until_image_appears,
    wait_until_image_disappears,
    is_image_on_screen,
)
from menu_downloader.screen_controller.screen_utils import (
    click_button
)
from menu_downloader.excel_controller.excel_utils import (
    is_on_excel_window
)
from menu_downloader.screen_controller.screen_time_consts import (
    TIME_INTERVAL_BETWWEN_CLICK_AND_KEYBOARD_CONTOL,
)
from menu_downloader.menu_controller.menu_path_director import (
    IMAGE_PATH_BAR_LOADING_IDENTIFIER,
    IMAGE_PATH_DATA_LENGTH_POPUP_IDENTIFIER
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
           wait_for_n_seconds(TIME_INTERVAL_BETWWEN_CLICK_AND_KEYBOARD_CONTOL)
           click_button(IMAGE_PATH_DATA_LENGTH_POPUP_IDENTIFIER)
        elif attempt >= max_retries:
            print('|- max retries reached. data loading did not complete.')
            return False
        elif is_on_excel_window():
            print('|- exception: excel is already running.')
            return False
        return is_now_bar_loading(max_retries, attempt + 1)

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