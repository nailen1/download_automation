
DATALAKE_DIR = r'C:\datalake'
FUND_CODE_DEFAULT = '000000'
BUCKET = 'dataset-system'
MAPPING_MENU_CODE_INPUT = {
    '2206': '2205',
}

# pseudo constants
FILE_FOLDER = lambda menu_code: f'dataset-menu{menu_code}'
FILE_NAME_FORMAT = lambda menu_code, fund_code, date_ref_nondashed, today_nondashed: f'menu{menu_code}-code{fund_code}-at{date_ref_nondashed}-save{today_nondashed}.csv'
BUCKET_PREFIX = FILE_FOLDER 
