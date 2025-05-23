from menu_downloader.screen_controller.screen_basis import (
    wait_for_n_seconds,
    wait_until_image_appears,
    wait_until_image_disappears,
    is_image_on_screen
)
from menu_downloader.menu_controller.menu_path_director import (
    IMAGE_PATH_CIRCLE_LOADING_IDENTIFIER,
)
from .menu_time_consts import TIME_INTERVAL_BETWEEN_PRESSING_LOAD_BUTTON_AND_LOADING

def is_circle_loading():
    return is_image_on_screen(image_path=IMAGE_PATH_CIRCLE_LOADING_IDENTIFIER, option_verbose=False)

def wait_until_circle_loading_appears(timeout=30, check_interval=1, option_verbose=False):
    return wait_until_image_appears(image_path=IMAGE_PATH_CIRCLE_LOADING_IDENTIFIER, timeout=timeout, check_interval=check_interval, option_verbose=option_verbose)

def wait_until_circle_loading_disappears(timeout=30, check_interval=1, option_verbose=False):
    return wait_until_image_disappears(image_path=IMAGE_PATH_CIRCLE_LOADING_IDENTIFIER, timeout=timeout, check_interval=check_interval, option_verbose=option_verbose)

def is_now_circle_loading(max_retries=30, attempt=1, timeout=5, check_interval=1):
    print(f'|- system loading ... (attempt {attempt})')
    wait_for_n_seconds(TIME_INTERVAL_BETWEEN_PRESSING_LOAD_BUTTON_AND_LOADING)
    if not is_circle_loading():
        print(f'|- assume system loaded instantly, i.e. within {TIME_INTERVAL_BETWEEN_PRESSING_LOAD_BUTTON_AND_LOADING}s.')
        return False
    loaded = wait_until_circle_loading_disappears(timeout=timeout, check_interval=check_interval)
    if loaded:
        print('|- system loaded.')
        return False
    else:
        if attempt >= max_retries:
            print('|- max retries reached. system loading did not complete.')
            return False
        return is_now_circle_loading(max_retries, attempt + 1)
