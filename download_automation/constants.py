# constants.py

import os
from dotenv import load_dotenv
from pyautogui import size

load_dotenv()

SCREEN_WIDTH, SCREEN_HEIGHT = size()

# Key constants
KEY_SAVE_AS_WINDOWS = 'F12'
FILE_FORMAT_SELECT_KEY = 'c'

# Folder paths
BASE_FOLDER_PATH = "C:\\datalake"

# Date constants
DATE_GENESIS = '2020-01-01'
DATE_GENESIS_REAL = '2020-05-28'

# Base directory
# BASE_DIR = os.path.abspath(os.path.dirname('__file__'))
BASE_DIR = "C:\\dev-system\\module-download_automation"

# Coordinate directory
COORDINATE_FOLDER = os.path.join(BASE_DIR, 'data', 'dataset-coordinate')

# Image paths
IMAGE_FOLDER = os.path.join(BASE_DIR, 'assets', 'image-system')

IMAGE_LOADING_SEARCH_GO = 'loading_search_go.png'
IMAGE_LOADING_EXCEL_GO = 'loading_excel_go.png'
IMAGE_EXCEL_HEADER = 'excel_header.png'
IMAGE_DATA_LENGTH_CAUTION_POPUP = 'data_length_caution_popup.png'
IMAGE_EXCEL_CAUTION_CONFIRM_BUTTON = 'excel_caution_confirm_button.png'
IMAGE_SAVE_CAUTION_POPUP = 'duplicated_name.png'
IMAGE_EXCEL_FOLDER_ARROWS = 'excel_folder_arrows.png'
IMAGE_NO_DATA_POPUP = 'no_data_popup.png'
IMAGE_SAVE_FORMAT_CONFIRM_BUTTON = 'save_format_confirm_button.png'
IMAGE_HEADER_BOS = 'header_bos.png'
IMAGE_HEADER_MOS = 'header_mos.png'
IMAGE_ICON_BOS = 'icon_bos.png'
IMAGE_ICON_MOS = 'icon_mos.png'
IMAGE_HEADER_LOGIN = 'header_login.png'
IMAGE_MOS_EXCEPTION_POPUP = 'mos_exception_popup.png'

IMAGE_PATH_LOADING_SEARCH_GO = os.path.join(IMAGE_FOLDER, IMAGE_LOADING_SEARCH_GO)
IMAGE_PATH_LOADING_EXCEL_GO = os.path.join(IMAGE_FOLDER, IMAGE_LOADING_EXCEL_GO)
IMAGE_PATH_EXCEL_HEADER = os.path.join(IMAGE_FOLDER, IMAGE_EXCEL_HEADER)
IMAGE_PATH_DATA_LENGTH_CAUTION_POPUP = os.path.join(IMAGE_FOLDER, IMAGE_DATA_LENGTH_CAUTION_POPUP)
IMAGE_PATH_EXCEL_CAUTION_CONFIRM_BUTTON = os.path.join(IMAGE_FOLDER, IMAGE_EXCEL_CAUTION_CONFIRM_BUTTON)
IMAGE_PATH_SAVE_CAUTION_POPUP = os.path.join(IMAGE_FOLDER, IMAGE_SAVE_CAUTION_POPUP)
IMAGE_PATH_EXCEL_FOLDER_ARROWS = os.path.join(IMAGE_FOLDER, IMAGE_EXCEL_FOLDER_ARROWS)
IMAGE_PATH_NO_DATA_POPUP = os.path.join(IMAGE_FOLDER, IMAGE_NO_DATA_POPUP)
IMAGE_PATH_SAVE_FORMAT_CONFIRM_BUTTON = os.path.join(IMAGE_FOLDER, IMAGE_SAVE_FORMAT_CONFIRM_BUTTON)
IMAGE_PATH_HEADER_BOS = os.path.join(IMAGE_FOLDER, IMAGE_HEADER_BOS)
IMAGE_PATH_HEADER_MOS = os.path.join(IMAGE_FOLDER, IMAGE_HEADER_MOS)
IMAGE_PATH_ICON_BOS = os.path.join(IMAGE_FOLDER, IMAGE_ICON_BOS)
IMAGE_PATH_ICON_MOS = os.path.join(IMAGE_FOLDER, IMAGE_ICON_MOS)
IMAGE_PATH_HEADER_LOGIN = os.path.join(IMAGE_FOLDER, IMAGE_HEADER_LOGIN)
IMAGE_PATH_MOS_EXCEPTION_POPUP = os.path.join(IMAGE_FOLDER, IMAGE_MOS_EXCEPTION_POPUP)

SYSTEM_INFO = os.getenv('SYSTEM_INFO')

PROCESS_NAME = '라이프자산운용'