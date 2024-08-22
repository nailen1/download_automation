# download_processor_for_excel.py

# External libraries
from shining_pebbles import *
from aws_s3_controller import *
from pyautogui import *
import psutil
import subprocess

# Internal modules
from screen_control_utils import *
from constants import *


# Screen size
screen_width, screen_height = size()

def is_on_running_excel():
    print('- (step) checking excel is running ...')
    wait_for_n_seconds(1)
    caution = check_image_appearance(IMAGE_PATH_EXCEL_HEADER, max_check_time=3)
    if caution:
        print('|- excel is running.')
        return True
    else:
        print('|- excel is not running.')
        return False

def is_on_excel_save_as_popup():
    print('- (step) checking excel save as popup ...')
    wait_for_n_seconds(2)
    caution = check_image_appearance(IMAGE_PATH_EXCEL_FOLDER_ARROWS, max_check_time=3)
    if caution:
        print('|- excel save as popup appeared.')
        return True
    else:
        print('|- no excel save as popup.')
        return False

def check_excel_execution():
    birth_confirmation = check_image_appearance(IMAGE_PATH_EXCEL_HEADER, max_check_time=10)
    wait_for_n_seconds(1)
    return birth_confirmation

def check_save_caution_popup():
    birth, death = check_image_birth_and_death(IMAGE_PATH_SAVE_CAUTION_POPUP, max_check_time_disappear=2)
    return birth

def check_folder_arrows():
    birth_confirmation = check_image_appearance(IMAGE_PATH_EXCEL_FOLDER_ARROWS, max_check_time=10)
    wait_for_n_seconds(1)
    return birth_confirmation

def close_excel():
    print(f'- (step) terminate Excel.')
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
    print(f"- (step) check existence of dataset")
    print(f"|- is '{regex_file_name}' downloaded in '{save_file_folder}'?")
    lst = scan_files_including_regex(save_file_folder, regex_file_name)
    if len(lst) == 0:
        print(f'|- no: {fund_code} not in {save_file_folder}')
        return False
    else:
        print(f'|- yes: {fund_code} in {save_file_folder}')
        return True

def control_on_excel_to_save_as_popup():
    if is_on_running_excel():
        pass
    else:
        control_on_excel_to_save_as_popup()
    print(f'- (step) open save as popup.')
    wait_for_n_seconds(2)
    press(KEY_SAVE_AS_WINDOWS)
    wait_for_n_seconds(1)

def control_on_save_as_popup(file_folder, file_name):
    if is_on_excel_save_as_popup():
        pass
    else: 
        raise Exception("No save as popup. Folder arrows not found.")

    print(f'- (step) input save settings.')
    typewrite(file_name)
    wait_for_n_seconds(1)
    press('tab')
    wait_for_n_seconds(1)
    typewrite(FILE_FORMAT_SELECT_KEY)
    wait_for_n_seconds(2)
    move_to_image(IMAGE_PATH_EXCEL_FOLDER_ARROWS)
    wait_for_n_seconds(2)
    move(screen_width/4,0)
    click()
    wait_for_n_seconds(2)
    typewrite(file_folder)
    wait_for_n_seconds(2)
    hotkey('alt', 's')
    if check_save_caution_popup():
        wait_for_n_seconds(1)
        hotkey('alt', 'y')
    else:
        print('- (step) save complete.')