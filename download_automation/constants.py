# constants.py

import os

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

IMAGE_PATH_LOADING_SEARCH_GO = os.path.join(IMAGE_FOLDER, IMAGE_LOADING_SEARCH_GO)
IMAGE_PATH_LOADING_EXCEL_GO = os.path.join(IMAGE_FOLDER, IMAGE_LOADING_EXCEL_GO)
IMAGE_PATH_EXCEL_HEADER = os.path.join(IMAGE_FOLDER, IMAGE_EXCEL_HEADER)
IMAGE_PATH_DATA_LENGTH_CAUTION_POPUP = os.path.join(IMAGE_FOLDER, IMAGE_DATA_LENGTH_CAUTION_POPUP)
IMAGE_PATH_EXCEL_CAUTION_CONFIRM_BUTTON = os.path.join(IMAGE_FOLDER, IMAGE_EXCEL_CAUTION_CONFIRM_BUTTON)
IMAGE_PATH_SAVE_CAUTION_POPUP = os.path.join(IMAGE_FOLDER, IMAGE_SAVE_CAUTION_POPUP)
IMAGE_PATH_EXCEL_FOLDER_ARROWS = os.path.join(IMAGE_FOLDER, IMAGE_EXCEL_FOLDER_ARROWS)
