# download_processor_for_excel.py

# External libraries
from shining_pebbles import *
from aws_s3_controller import *
from pyautogui import size, press, hotkey, typewrite, move, click
import psutil
import subprocess
from menu_downloader.screen_controller.screen_basis import (
    wait_for_n_seconds,
    wait_until_image_appears,
    move_to_image,
    is_image_on_screen,
)
from menu_downloader.excel_controller.excel_path_director import (
    IMAGE_PATH_EXCEL_IDENTIFIER,
    IMAGE_PATH_SAVE_CAUTION_POPUP,
    IMAGE_PATH_EXCEL_FOLDER_ARROWS,
    IMAGE_PATH_EXCEL_SAVE_AS_POPUP_IDENTIFIER
)
from .excel_consts import (
    KEY_SAVE_AS_WINDOWS,
    FILE_FORMAT_SELECT_KEY
)

def is_on_excel_window():
    return is_image_on_screen(image_path=IMAGE_PATH_EXCEL_IDENTIFIER, option_verbose=False)

def is_on_excel_save_as_popup():
    return is_image_on_screen
    
def is_excel_save_caution_popup():
    return is_image_on_screen(image_path=IMAGE_PATH_SAVE_CAUTION_POPUP, option_verbose=False)

def is_on_running_excel():
    print('| (step) checking excel is running ...')
    wait_for_n_seconds(1)
    caution = wait_until_image_appears(IMAGE_PATH_EXCEL_IDENTIFIER, max_check_time=3)
    if caution:
        print('|- excel is running.')
        return True
    else:
        print('|- excel is not running.')
        return False

def is_on_excel_save_as_popup():
    print('| (step) checking excel save as popup ...')
    wait_for_n_seconds(2)
    save_as_popup = wait_until_image_appears(IMAGE_PATH_EXCEL_SAVE_AS_POPUP_IDENTIFIER, max_check_time=3)
    if save_as_popup:
        print('|- excel save as popup appeared.')
        return True
    else:
        print('|- no excel save as popup.')
        return False

def check_folder_arrows():
    folder_arrows = wait_until_image_appears(IMAGE_PATH_EXCEL_FOLDER_ARROWS, max_check_time=10)
    wait_for_n_seconds(1)
    return folder_arrows

def close_excel():
    print(f'| (step) terminate Excel.')
    wait_for_n_seconds(2)
    subprocess.run(['taskkill', '/F', '/IM', 'excel.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def get_excel_process_count():
    """Returns the number of running Excel processes."""
    count = 0
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'EXCEL.EXE':
            count += 1
    return count

def kill_all_excel_processes():
    """Kills all running Excel processes."""
    subprocess.run(['taskkill', '/F', '/IM', 'excel.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def check_excel_processes_status_and_quit_all(n=3):
    excel_count = get_excel_process_count()    
    if excel_count >= n:
        print(f"    Caution! There are {excel_count} Excel processes running. Terminating all Excel processes.")
        kill_all_excel_processes()
        wait_for_n_seconds(5)
    else:
        print(f"    There are only {excel_count} Excel processes running. No action needed.")

def goto_home():
    wait_for_n_seconds(2)
    print(f'(step) finish download cycle.')
    print()

def is_dataset_downloaded(fund_code, save_file_folder, file_name):
    regex_file_name = file_name.split('.csv')[0][:-1]
    print(f"| (step) check existence of dataset")
    print(f"|- is '{regex_file_name}' downloaded in '{save_file_folder}'?")
    lst = scan_files_including_regex(save_file_folder, regex_file_name)
    if len(lst) == 0:
        print(f'|- no: {fund_code} not in {save_file_folder}')
        return False
    else:
        print(f'|- yes: {fund_code} in {save_file_folder}')
        return True
    
def delete_file(file_folder, file_name):
    file_path = os.path.join(file_folder, file_name)
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"{file_path} deleted.")
    else:
        print(f"{file_path} not found.")


def control_on_excel_to_save_as_popup():
    if is_on_running_excel():
        pass
    else:
        control_on_excel_to_save_as_popup()
    print(f'| (step) open save as popup.')
    wait_for_n_seconds(2)
    press(KEY_SAVE_AS_WINDOWS)
    wait_for_n_seconds(1)

def control_on_save_as_popup(file_folder, file_name):
    if is_on_excel_save_as_popup():
        pass
    else: 
        raise Exception("No save as popup. Folder arrows not found.")

    print(f'| (step) input save settings.')
    typewrite(file_name)
    wait_for_n_seconds(1)
    press('tab')
    wait_for_n_seconds(1)
    typewrite(FILE_FORMAT_SELECT_KEY)
    wait_for_n_seconds(2)
    move_to_image(IMAGE_PATH_EXCEL_FOLDER_ARROWS)
    wait_for_n_seconds(2)
    screen_width, screen_height = size()
    move(screen_width/4,0)
    click()
    wait_for_n_seconds(2)
    typewrite(file_folder)
    wait_for_n_seconds(2)
    hotkey('alt', 's')
    if is_excel_save_caution_popup():
        wait_for_n_seconds(1)
        hotkey('alt', 'y')
    else:
        print('| (step) save complete.')