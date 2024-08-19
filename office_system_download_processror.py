# version20240808 refactioing

from shining_pebbles import *
from aws_s3_controller import *
from screen_coordinates_utils import *
from coordinate_tracer import *
import os
import pyautogui
from pyautogui import *
import time
import psutil
import subprocess



# key constants
key_save_as_windows = 'F12'
file_format_select_key = 'c'

# folder paths
base_folder_path = "C:\\datalake"

# screen size
screen_width, screen_height = size()

# image paths
image_folder = './image-system'
image_loading_search_go = 'image-loading-search-go.png'
image_loading_excel_go = 'image-loading-excel-go.png'
image_excel_header = 'image-excel-header.png'
image_data_length_caution_popup = 'image-data-length-caution-popup.png'
image_excel_caution_confirm_button = 'image-excel-caution-confirm-button.png'
image_save_caution_popup = 'image-duplicated-name.png'
image_excel_folder_arrows = 'image-excel-folder-arrows.png'
image_path_loading_search_go = os.path.join(image_folder, image_loading_search_go)
image_path_loading_excel_go = os.path.join(image_folder, image_loading_excel_go)
image_path_excel_header = os.path.join(image_folder, image_excel_header)
image_path_data_length_caution_popup = os.path.join(image_folder, image_data_length_caution_popup)
image_path_excel_caution_confirm_button = os.path.join(image_folder, image_excel_caution_confirm_button)
image_path_save_caution_popup = os.path.join(image_folder, image_save_caution_popup)
image_path_excel_folder_arrows = os.path.join(image_folder, image_excel_folder_arrows)


# date constants
date_genesis = '2020-01-01'
date_genesis_real = '2020-05-28'


def is_now_search_loading():
    print('-- search loading ...')
    wait_for_n_seconds(1)
    loading = check_image_appearance(image_path_loading_search_go, max_check_time=5)
    if loading:
        is_now_search_loading()
    else:
        print('-- search loaded.')
        return False


def is_now_data_loading():
    print('-- data loading ...')
    loading = check_image_appearance(image_path_loading_excel_go, max_check_time=5)
    if loading:
        if is_there_data_length_caution_popup():
            wait_for_n_seconds(2)
            move_to_image(image_path_excel_caution_confirm_button)
            wait_for_n_seconds(1)
            click()
        is_now_data_loading()
    else:
        print('-- data loaded.')
        return False


def is_there_data_length_caution_popup():
    print('-- checking data length caution popup ...')
    wait_for_n_seconds(1)
    caution = check_image_appearance(image_path_data_length_caution_popup, max_check_time=3)
    if caution:
        print('-- data length caution popup appeared.')
        return True
    else:
        print('-- no data length caution popup.')
        return False

def is_on_running_excel():
    print('-- checking excel is running ...')
    wait_for_n_seconds(1)
    caution = check_image_appearance(image_path_excel_header, max_check_time=3)
    if caution:
        print('-- excel is running.')
        return True
    else:
        print('-- excel is not running.')
        return False

def is_on_excel_save_as_popup():
    print('-- checking excel save as popup ...')
    wait_for_n_seconds(2)
    caution = check_image_appearance(image_path_excel_folder_arrows, max_check_time=3)
    if caution:
        print('-- excel save as popup appeared.')
        return True
    else:
        print('-- no excel save as popup.')
        return False


def is_there_error_in_dataset_menu2160(file_folder, file_name):
    df = open_df_in_file_folder_by_regex(file_folder=file_folder, file_name=file_name)
    row = len(df.dropna())
    if row == 0:
        print(f'-- Error in dataset')
        return True
    else:
        print(f'-- No error in dataset')
        return False

def check_excel_execution():
    birth_confirmation = check_image_appearance(image_path_excel_header, max_check_time=10)
    wait_for_n_seconds(1)
    return birth_confirmation

def check_save_caution_popup():
    birth, death = check_image_birth_and_death(image_path_save_caution_popup, max_check_time_disappear=2)
    return birth

def check_folder_arrows():
    birth_confirmation = check_image_appearance(image_path_excel_folder_arrows, max_check_time=10)
    wait_for_n_seconds(1)
    return birth_confirmation

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
        print(f"- Caution! There are {excel_count} Excel processes running. Terminating all Excel processes.")
        kill_all_excel_processes()
        wait_for_n_seconds(5)
    else:
        print(f"- There are only {excel_count} Excel processes running. No action needed.")

def is_dataset_downloaded(fund_code, save_file_folder, file_name):
    regex_file_name = file_name.split('.csv')[0][:-1]
    print(f"- is dataset '{regex_file_name}' downloaded in '{save_file_folder}'?")
    lst = scan_files_including_regex(save_file_folder, regex_file_name)
    if len(lst) == 0:
        print(f'-- no: {fund_code} not in {save_file_folder}')
        return False
    else:
        print(f'-- yes: {fund_code} in {save_file_folder}')
        return True
    
def move_to_image(image_path, confidence_level=0.8, timeout=10):
    start_time = time.time()
    while True:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence_level)
            if location:
                pyautogui.moveTo(location)
                return True
        except ImageNotFoundException:
            # 이미지를 찾지 못한 경우, 예외 처리로 False 반환
            print(f"- Could not find the image '{image_path}'. Assuming it is not present.")
            return False

        # 현재 시간과 시작 시간의 차이가 timeout보다 크면 종료
        if time.time() - start_time > timeout:
            print(f"- Timeout! Could not find the image '{image_path}' within {timeout} seconds.")
            return False
        
        time.sleep(1)


def close_excel():
    print(f'- step: terminate Excel.')
    wait_for_n_seconds(2)
    subprocess.run(['taskkill', '/F', '/IM', 'excel.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def goto_home():
    wait_for_n_seconds(2)
    print(f'- step: finish download cycle.')
    print()


# EXCEL GENERAL
def control_on_excel_to_save_as_popup():
    if is_on_running_excel():
        pass
    else:
        control_on_excel_to_save_as_popup()
    print(f'- step: open save as popup.')
    wait_for_n_seconds(2)
    press(key_save_as_windows)
    wait_for_n_seconds(1)


def control_on_save_as_popup(file_folder, file_name):
    if is_on_excel_save_as_popup():
        pass
    else: 
        raise Exception("No save as popup. Folder arrows not found.")

    print(f'- step: input save settings.')
    typewrite(file_name)
    wait_for_n_seconds(1)
    press('tab')
    wait_for_n_seconds(1)
    typewrite(file_format_select_key)
    wait_for_n_seconds(2)
    move_to_image(image_path_excel_folder_arrows)
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
        print('- step: download complete.')


def delete_file(file_folder, file_name):
    file_path = os.path.join(file_folder, file_name)
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"{file_path} deleted.")
    else:
        print(f"{file_path} not found.")


# S3 UPLOAD GENERAL
def validate_download_process(file_folder, file_name, exception=False):
    print(f'- step: validate download process.')
    if exception:
        return True
    df = open_df_in_file_folder_by_regex(file_folder=file_folder, regex=file_name)
    shape = df.iloc[:, :2].dropna().shape
    rows = shape[0]
    print(f'-- {rows} rows in dataset.')
    if rows > 0:
        print(f'- step: download complete.')
        return True
    else:
        print(f'- step: download failed.')
        return False
    
    
def upload_downloaded_dataset_to_s3(file_folder, file_name, bucket_prefix, bucket='dataset-system'):
    upload_files_to_s3(file_folder_local=file_folder, regex=file_name, bucket=bucket, bucket_prefix=bucket_prefix)
    print(f'- step: uploading dataset to S3://{bucket}/{bucket_prefix} complete.')


def get_input_dates_downloaded_in_file_folder(menu_code, file_folder=None, form='%Y%m%d'):
    file_folder = os.path.join(base_folder_path, f'dataset-menu{menu_code}') if file_folder is None else file_folder
    file_names_downloaded = scan_files_including_regex(file_folder=file_folder, regex=f'menu{menu_code}')
    input_dates_downloaded = [pick_input_date_in_file_name(file_name) for file_name in file_names_downloaded]
    if form == '%Y-%m-%d':
        input_dates_downloaded = [f'{date[:4]}-{date[4:6]}-{date[6:8]}' for date in input_dates_downloaded]
    return input_dates_downloaded

