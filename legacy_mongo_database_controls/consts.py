import os
from dotenv import load_dotenv

load_dotenv()
MY_MONGO_URI = os.getenv('MY_MONGO_URI')
BASE_DIR_FUND = os.getenv('BASE_DIR_FUND')
BASE_DIR_DART = os.getenv('BASE_DIR_DART')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEGACY_DATABASE_NAME = 'database-rpa'
ACTUAL_GENESIS_DATE = '2020-05-26'