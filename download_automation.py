from coordinate_tracer import *
from shining_pebbles import *
from office_system_download_processror import *

def get_df_coordinate_of_menu(menu_code):
    df = open_recorded_coordinates(file_folder='dataset-coordinate', subject=f'menu{menu_code}')
    return df

def get_sequences_of_menu(menu_code):
    df = get_df_coordinate_of_menu(menu_code)
    sequences = list(df['sequence'])
    return sequences

def get_coordinates_of_menu(menu_code, coord_type='absolute_coord'):
    df = get_df_coordinate_of_menu(menu_code)
    coordinates = list(df[coord_type])
    return coordinates

def get_mapping_sequence_to_coordinate_of_menu(menu_code, coord_type='absolute_coord'):
    df = get_df_coordinate_of_menu(menu_code)
    dct = df.set_index('sequence')[coord_type].to_dict()
    return dct

def export_data_info_of_sequence_and_coordinate_of_menu(menu_code):
    df = get_df_coordinate_of_menu(menu_code)
    info = df.to_dict(orient='records')
    dct = {
        'menu_code': menu_code,
        'info': info
    }
    return dct

def input_something_on_input_field(coord_input, something, verbose=False):
    if verbose:
        print(f'- input {something}')
    wait_for_n_seconds(1)
    click(coord_input)
    hotkey('ctrl', 'a')
    wait_for_n_seconds(0.5)
    press('backspace')
    wait_for_n_seconds(0.5)
    typewrite(list(something))
    return None

def execute_input_menu_code_of_menu_and_enter(coord_input_menu, menu_code):
    input_something_on_input_field(coord_input=coord_input_menu, something=menu_code)
    wait_for_n_seconds(0.5)
    press('enter')
    wait_for_n_seconds(1)
    return None

def execute_input_fund_code(coord_input_fund_code, fund_code):
    input_something_on_input_field(coord_input=coord_input_fund_code, something=fund_code)
    return None

def execute_input_end_date_by_coord(coord_input_end_date, end_date):
    input_something_on_input_field(coord_input=coord_input_end_date, something=end_date)
    return None

def click_button(coord_button, verbose=False):
    if verbose:
        print(f'- click button')
    wait_for_n_seconds(1)
    click(coord_button)
    return None


# key constants
key_save_as_windows = 'F12'
file_format_select_key = 'c'

# folder paths
base_folder_path = "C:\\datalake"

# screen size
screen_width, screen_height = size()

# menu codes constants
menu_codes_snapshot = ['2160', '2205', '2820', '8186']
menu_codes_period = ['4165', '4604']

# date constants
date_genesis = '2020-01-01'
date_genesis_real = '2020-05-28'


class MOS:
    def __init__(self, menu_code, fund_code=None,  input_date=None, start_date=None, end_date=None, file_folder=None, file_name=None):
        self.menu_code = menu_code
        self.fund_code = fund_code or ''
        self.input_date = input_date.replace("-","") if input_date !=None else self.set_default_input_date()
        self.start_date = start_date.replace("-","") if start_date !=None else self.set_default_start_date()
        self.end_date = end_date.replace("-","") if end_date !=None else self.set_default_end_date()
        self.df_coordinate = self.get_df_coordinate()
        self.coordinates = self.get_coordinates()
        self.relative_coordinates = self.get_relative_coordinates()
        self.file_folder = self.set_file_folder(file_folder=file_folder)
        self.file_name = self.set_file_name(file_name=file_name)
        self.bucket_name = 'dataset-system'
        self.bucket_prefix = self.set_bucket_prefix()


    def set_default_input_date(self):
        if self.start_date == self.end_date and self.end_date != None:
            input_date = self.end_date.replace("-","")
        else:
            raise ValueError('No valid input date')
        return input_date    
    
    def set_default_start_date(self):
        start_date = date_genesis.replace("-","") if self.input_date == None else self.input_date
        return start_date
    
    def set_default_end_date(self):
        end_date = get_today("%Y%m%d").replace("-","") if self.input_date == None else self.input_date
        return end_date
    
    
    def set_file_folder(self, file_folder=None):
        file_folder_default = f'dataset-menu{self.menu_code}' if file_folder == None else f'dataset-save{get_today(form="yyyymmdd")}'
        if self.input_date and self.fund_code=='' and self.menu_code in menu_codes_snapshot:
            file_folder_default = f'dataset-menu{self.menu_code}-snapshot'
        file_folder_path = os.path.join(base_folder_path, file_folder_default) if file_folder == None else file_folder  
        check_folder_and_create_folder(file_folder_path)
        self.file_folder = file_folder_path
        return file_folder_path
    

    def set_file_name(self, file_name=None):
        fund_code_value = '000000' if self.fund_code == '' else self.fund_code
        self.file_name_timeseries = f'menu{self.menu_code}-code{fund_code_value}-from{self.start_date}-to{self.end_date}-save{get_today(form="yyyymmdd")}.csv'
        self.file_name_snapshot = f'menu{self.menu_code}-code{fund_code_value}-at{self.end_date}-save{get_today(form="yyyymmdd")}.csv'
        self.file_name_period = f'menu{self.menu_code}-code{fund_code_value}-between{self.start_date}-and{self.end_date}-save{get_today(form="yyyymmdd")}.csv'

        if not self.input_date and self.menu_code:
            file_name = self.file_name_timeseries
        elif self.menu_code in menu_codes_period:
            file_name = self.file_name_period

        if self.input_date:
            file_name = self.file_name_snapshot
 
        if file_name is not None:
            file_name = file_name

        self.file_name = file_name
        return file_name
    

    def set_bucket_prefix(self):
        bucket_prefix = f'dataset-menu{self.menu_code}'
        if self.file_name == self.file_name_snapshot and self.menu_code:
            bucket_prefix = f'dataset-menu{self.menu_code}'
        if self.file_name == self.file_name_snapshot and self.menu_code in menu_codes_snapshot:
            bucket_prefix = f'dataset-menu{self.menu_code}-snapshot'
        self.bucket_prefix = bucket_prefix
        return bucket_prefix

    def get_df_coordinate(self):
        df = get_df_coordinate_of_menu(self.menu_code)
        self.df_coordinate = df
        return df

    def get_sequences(self):
        sequences = get_sequences_of_menu(self.menu_code)
        self.sequences = sequences
        return sequences

    def get_coordinates(self):
        coordinates = get_coordinates_of_menu(self.menu_code, coord_type='absolute_coord')
        self.coordinates = coordinates
        return coordinates
    
    def get_relative_coordinates(self):
        coordinates = get_coordinates_of_menu(self.menu_code, coord_type='relative_coord')
        self.relative_coordinates = coordinates
        return coordinates

    def get_mapping_sequence_to_coordinate(self, coord_type='absolute_coord'):
        dct = get_mapping_sequence_to_coordinate_of_menu(self.menu_code, coord_type=coord_type)
        self.mapping_sequence_to_coordinate = dct
        return dct
    
    def get_coord_of_sequence(self, sequence):
        if not hasattr(self, 'mapping_sequence_to_coordinate'):
            self.get_mapping_sequence_to_coordinate()
        mapping = self.mapping_sequence_to_coordinate
        coord = mapping[sequence]
        return coord

    def execute_input_menu_code(self):
        print(f'- open menu: {self.menu_code}')
        coord = self.get_coord_of_sequence('input_menu_code')
        execute_input_menu_code_of_menu_and_enter(coord_input_menu=coord, menu_code=self.menu_code)
        return None
    
    def execute_input_fund_code(self):
        fund_code_value = '000000 == all funds' if self.fund_code == '' else self.fund_code
        print(f'- input fund code: {fund_code_value}')
        coord = self.get_coord_of_sequence('input_fund_code')
        execute_input_fund_code(coord_input_fund_code=coord, fund_code=self.fund_code)
        return None
    
    def execute_input_start_date(self):
        print(f'- input start date: {self.start_date}')
        coord = self.get_coord_of_sequence('input_start_date')
        input_something_on_input_field(coord_input=coord, something=self.start_date)
        return None
    
    def execute_input_end_date(self):
        print(f'- input end date: {self.end_date}')
        coord = self.get_coord_of_sequence('input_end_date')
        input_something_on_input_field(coord_input=coord, something=self.end_date)
        return None
    
    def execute_input_ref_date(self):
        print(f'- input ref date: {self.input_date}')
        coord = self.get_coord_of_sequence('input_ref_date')
        input_something_on_input_field(coord_input=coord, something=self.input_date)
        return None
    
    def execute_button_search(self):
        print(f'- click search button')
        coord = self.get_coord_of_sequence('button_search')
        click_button(coord_button=coord)
        if not is_now_search_loading():
            pass
        wait_for_n_seconds(3)
        return None
    
    def execute_button_excel(self):
        print(f'- click excel button')
        coord = self.get_coord_of_sequence('button_excel')
        mapping = self.mapping_sequence_to_coordinate
        click_button(coord_button=coord)
        if 'button_excel_popup' not in mapping.keys():
            if not is_now_data_loading():
                pass
            wait_for_n_seconds(3)
        return None

    def execute_button_excel_popup(self):
        print(f'- click excel popup button')
        coord = self.get_coord_of_sequence('button_excel_popup')
        click_button(coord_button=coord)
        if not is_now_data_loading():
            pass
        wait_for_n_seconds(3)
        return None

    def execute_process_on_excel(self):  
        control_on_excel_to_save_as_popup()
        control_on_save_as_popup(file_folder=self.file_folder, file_name=self.file_name)
        wait_for_n_seconds(3)
        close_excel()
        wait_for_n_seconds(2)
        if validate_download_process(self.file_folder, self.file_name):
            upload_downloaded_dataset_to_s3(self.file_folder, self.file_name, bucket_prefix=self.bucket_prefix)
        else:
            delete_file(self.file_folder, self.file_name)
        check_excel_processes_status_and_quit_all()
        return None
            
    def execute_sequence(self, sequence):
        if not hasattr(self, 'mapping_sequence_to_coordinate'):
            self.get_mapping_sequence_to_coordinate()
        mapping_sequence = {
            'input_menu_code': self.execute_input_menu_code,
            'input_fund_code': self.execute_input_fund_code,
            'input_start_date': self.execute_input_start_date,
            'input_end_date': self.execute_input_end_date,
            'input_ref_date': self.execute_input_ref_date,
            'button_search': self.execute_button_search,
            'button_excel': self.execute_button_excel,
            'button_excel_popup': self.execute_button_excel_popup,
        }
        return mapping_sequence[sequence]()
    
    def execute_all_sequences(self):
        if not hasattr(self, 'sequences'):
            self.get_sequences()
        for sequence in self.sequences:
            self.execute_sequence(sequence)
        self.execute_process_on_excel()
        return None
    
    def recursive_download_dataset(self):
        if is_dataset_downloaded(fund_code=self.file_folder, save_file_folder=self.file_folder, file_name=self.file_name):
            print(f'⭕ download complete: {self.file_name} in {self.file_folder}')
            close_excel()
        else:
            self.execute_all_sequences()
            self.recursive_download_dataset()
        return None
    
        
def download_all_snapshot_datasets_of_timeseries(menu_code, start_date=date_genesis_real, end_date=get_date_n_days_ago(get_today("%Y-%m-%d"),1)):
    dates = get_date_range(start_date_str=start_date, end_date_str=end_date)
    dates_downloaded = get_input_dates_downloaded_in_file_folder(menu_code, file_folder=os.path.join(base_folder_path, f'dataset-menu{menu_code}-snapshot'), form='%Y-%m-%d')
    if dates_downloaded != []:
        print(f'{len(dates_downloaded)}/{len(dates)} dates downloaded: ... {dates_downloaded[-1]}')
        dates = sorted(list(set(dates) - set(dates_downloaded)))
    dates = sorted(dates, reverse=True)
    for date in tqdm(dates):
        print(f' ▶ input date: {date}')
        mos = MOS(menu_code=menu_code, input_date=date)
        mos.recursive_download_dataset()
    return None