
DATALAKE_DIR = r'C:\datalake'
FUND_CODE_DEFAULT = '000000'
BUCKET = 'dataset-system'
MAPPING_MENU_CODE_INPUT = {
    '2206': '2205',
    '1101': '1100',
    '1102': '1100',
    '1103': '1100',
    '1104': '1100',
    '1105': '1100',
}

# pseudo constants
FILE_FOLDER = lambda menu_code: f'dataset-menu{menu_code}'
SNAPSHOT_FILE_NAME_FORMAT = lambda menu_code, fund_code, date_ref_nondashed, today_nondashed: f'menu{menu_code}-code{fund_code}-at{date_ref_nondashed}-save{today_nondashed}.csv'
TIMESERIES_FILE_NAME_FORMAT = lambda menu_code, fund_code, start_date_nondashed, end_date_nondashed, today_nondashed: f'menu{menu_code}-code{fund_code}-from{start_date_nondashed}-to{end_date_nondashed}-save{today_nondashed}.csv'
BUCKET_PREFIX = FILE_FOLDER 
