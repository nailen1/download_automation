import pygetwindow as gw
from pyautogui import typewrite, press
import subprocess

from .constants import *
from .screen_control_utils import *
from .download_processor_for_office_system import *


def get_operating_windows_by_title(title):
    windows = gw.getWindowsWithTitle(title)
    return windows

def activate_window(window):
    window.minimize()
    window.restore()
    window.activate()
    return None

def is_this_window_mos(window):
    activate_window(window)
    wait_for_n_seconds(0.5)
    if find_image_on_screen(IMAGE_PATH_HEADER_MOS):
        return True
    else:
        return False
    
def is_this_window_bos(window):
    activate_window(window)
    wait_for_n_seconds(0.5)
    if find_image_on_screen(IMAGE_PATH_HEADER_BOS):
        return True
    else:
        return False
   
def assign_office_system_type(windows):
    dct_window = {}
    for window in windows:
        if is_this_window_mos(window):
            dct_window['MOS'] = window
            print('|- set operating window as mos')
        elif is_this_window_bos(window):
            dct_window['BOS'] = window
            print('|- set operating window as bos')
        window.minimize()
        wait_for_n_seconds(0.5)
    return dct_window

def set_default_setting(window):
    activate_window(window)
    wait_for_n_seconds(0.5)
    locate_window(window, coord_x=0, coord_y=0)
    wait_for_n_seconds(0.5)
    resize_window(window, ratio_x=0.5, ratio_y=1)
    wait_for_n_seconds(0.5)
    return None

def locate_window(window, coord_x=0, coord_y=0):
    print(f'|-- locating window at ({coord_x}, {coord_y})')
    window.moveTo(coord_x, coord_y)
    return None

def resize_window(window, ratio_x, ratio_y):
    new_width = int(SCREEN_WIDTH * ratio_x)
    new_height = int(SCREEN_HEIGHT * ratio_y)
    print(f'|-- resizing window to ({new_width}, {new_height})')
    window.resizeTo(new_width, new_height)
    return None

def click_icon_of_system(name_system):
    mapping_name_to_image = {
        'MOS': IMAGE_PATH_ICON_MOS,
        'BOS': IMAGE_PATH_ICON_BOS,
    }
    move_to_image(mapping_name_to_image[name_system])
    click()
    return None

def check_login_window_of_system(name_system):
    wait_for_n_seconds(1)
    if name_system == 'MOS':
        wait_for_n_seconds(2)
        press('enter')
    if not is_now_data_loading():
        wait_for_n_seconds(1)
        if find_image_on_screen(IMAGE_PATH_HEADER_LOGIN):
            print(f'|- ({name_system}) login window is found')
            return True
        else:
            return False

def login_on_system():
    typewrite(SYSTEM_INFO)
    wait_for_n_seconds(1)
    press('enter')
    print('|-- logging in system ... ')
    return None

def check_system_is_running(name_system):
    wait_for_n_seconds(1)
    mapping_name_to_image = {
        'MOS': IMAGE_PATH_ICON_MOS,
        'BOS': IMAGE_PATH_ICON_BOS,
    }
    if find_image_on_screen(mapping_name_to_image[name_system]):
        print(f'|- ({name_system}) is running ... ')
        return True
    else:
        print(f'|- ({name_system}) is not running ... ')
        return False

def execute_system(name_system):
    click_icon_of_system(name_system)
    if name_system == 'MOS':
        if is_there_mos_exception_popup():
            wait_for_n_seconds(1)
            press('enter')
        elif is_loading_completed():
            wait_for_n_seconds(1)
            press('enter') 
    if is_on_login_window():
        login_on_system()
    if check_system_is_running(name_system):
        wait_for_n_seconds(3)
        print(f'|- ({name_system}) is running ... ')
        return True
    else:
        return False

def close_system():
    print(f'| (step) terminate office systems.')
    wait_for_n_seconds(2)
    subprocess.run(['taskkill', '/F', '/IM', 'XPlatform.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return None