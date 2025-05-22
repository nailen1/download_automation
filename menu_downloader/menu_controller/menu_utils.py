from pyautogui import press
from menu_downloader.screen_controller.screen_basis import (
    wait_for_n_seconds,
    check_image_appearance,
)
from menu_downloader.screen_controller.screen_utils import (
    input_something_on_input_field,
)
from menu_downloader.screen_controller.screen_time_consts import (
    TIME_INTERVAL_BETWWEN_TYPING_AND_ENTER,
    TIME_INTERVAL_BETWWEN_TYPING_AND_ENTER_LONG,
)
from .menu_path_director import (
    IMAGE_PATH_LOADING_SEARCH_GO
)
def execute_input_menu_code_and_press_enter(coord_input_menu, menu_code):
    input_something_on_input_field(coord_input=coord_input_menu, something=menu_code)
    wait_for_n_seconds(TIME_INTERVAL_BETWWEN_TYPING_AND_ENTER)
    press('enter')
    return None

# def execute_input_fund_code_on_coord(coord_input_fund_code, fund_code):
#     input_something_on_input_field(coord_input=coord_input_fund_code, something=fund_code)
#     return None

# def execute_input_date_on_coord(coord_input_date, date):
#     input_something_on_input_field(coord_input=coord_input_date, something=date)
#     return None


def check_loading(max_check_time=30, check_interval=1, option_verbose=False):
    return check_image_appearance(image_path=IMAGE_PATH_LOADING_SEARCH_GO, max_check_time=max_check_time, check_interval=check_interval, option_verbose=option_verbose)


def is_now_search_loading(max_retries=30, attempt=1, max_check_time=5, check_interval=5):
    print(f'|- search loading ... (attempt {attempt})')
    wait_for_n_seconds(1)
    loading = check_loading(max_check_time=max_check_time, check_interval=check_interval)
    if loading:
        if attempt >= max_retries:
            print('|- max retries reached. search loading did not complete.')
            return False
        return is_now_search_loading(max_retries, attempt + 1)
    else:
        print('|- search loaded.')
        return False