# download_automation.py

from shining_pebbles import *

from .coordinate_tracer import *
from .download_processor_for_office_system import *
from .download_processor_for_excel import *
from .download_processor_for_s3 import *
from .constants import *
from .download_processor_for_excel import delete_file


# # screen size
screen_width, screen_height = size()

# # menu codes constants
menu_codes_snapshot = ['2160', '2205', '2820', '8186', '4604']
menu_codes_period = ['4165', '4604', '4110']
menu_codes_having_fast_excel_execution = ['4604', '2205', '2820']
menu_codes_validate_exception = ['4604', '2820'] 

MENU_CODES_SNAPSHOT = ['2205']
MENU_CODES_TIMESERIES_BUT_SNAPSHOT = ['2160', '2820', '8186', '4165']
MENU_CODES_PERIOD = ['4165', '4604', '4110', '8870']
MENU_CODES_HAVING_FAST_EXCEL_EXECUTION = ['4604', '2205', '2820']
MENU_CODES_VALIDATE_EXCEPTION = ['4604', '2820']

BUCKET_NAME_SYSYTEM = 'dataset-system'


class OfficeSystem:
    def __init__(self, menu_code, fund_code=None,  input_date=None, start_date=None, end_date=None, file_folder=None, file_name=None):
        self.menu_code = self.set_menu_code(menu_code)
        self.fund_code =self.set_default_fund_code(fund_code)
        self.date = self.set_default_dates(input_date, start_date, end_date, menu_code)
        self.input_date = self.date['input_date']
        self.start_date = self.date['start_date']
        self.end_date = self.date['end_date']
        self.file_folder = self.set_default_file_folder(menu_code, self.fund_code, file_folder)
        self.file_name = self.set_default_file_name(file_name)
        self.bucket = self.set_bucket()
        self.bucket_prefix = self.set_bucket_prefix()
        self.df_coordinate = self.get_df_coordinate()
        self.coordinates = self.get_coordinates()
        self.relative_coordinates = self.get_relative_coordinates()
        
    def set_menu_code(self, menu_code):
        mapping_menu_code = {
            '2205s': '2205'
        }
        self.menu_code = mapping_menu_code.get(menu_code, menu_code) or ''
        self.menu_code_present = menu_code
        print('self.menu_code', self.menu_code)
        print('self.menu_code_present', self.menu_code_present)
        return self.menu_code
    
    def set_default_fund_code(self, fund_code):
        fund_code = fund_code or ''
        self.fund_code = fund_code
        return fund_code

    def set_default_dates(self, input_date, start_date, end_date, menu_code):
        date = set_dates_by_initial_inputs(input_date, start_date, end_date, menu_code) 
        self.input_date = date['input_date']
        self.start_date = date['start_date']
        self.end_date = date['end_date']
        return date
    
    def set_default_file_folder(self, menu_code, fund_code, file_folder=None):
        file_folder = set_file_folder(menu_code, fund_code) if file_folder == None else file_folder
        file_folder_path = os.path.join(BASE_FOLDER_PATH, file_folder)
        check_folder_and_create_folder(file_folder_path)
        self.file_folder_name = file_folder
        self.file_folder = file_folder_path
        return file_folder_path
    
    def set_default_file_name(self, file_name=None):
        fund_code_in_file_name = '000000' if self.fund_code == '' else self.fund_code
        file_name_snapshot = f'menu{self.menu_code_present}-code{fund_code_in_file_name}-at{self.input_date}-save{get_today(form="yyyymmdd")}.csv'
        file_name_timeseries = f'menu{self.menu_code_present}-code{fund_code_in_file_name}-from{self.start_date}-to{self.end_date}-save{get_today(form="yyyymmdd")}.csv'
        file_name_period = f'menu{self.menu_code_present}-code{fund_code_in_file_name}-between{self.start_date}-and{self.end_date}-save{get_today(form="yyyymmdd")}.csv'

        if self.input_date != None:
            file_name = file_name_snapshot
        elif self.menu_code in MENU_CODES_PERIOD:
            file_name = file_name_period
        else:
            file_name = file_name_timeseries 

        self.file_name = file_name
        return file_name
    
    def set_bucket(self):
        bucket = BUCKET_NAME_SYSYTEM
        self.bucket = bucket
        return bucket

    def set_bucket_prefix(self):
        bucket_prefix = self.file_folder_name
        self.bucket_prefix = bucket_prefix
        return bucket_prefix


    # def set_default_input_date(self, input_date, start_date, end_date):
    #     if input_date == None:
    #         if end_date != None and start_date == end_date:    
    #             input_date = end_date.replace("-","")
    #         else:
    #             input_date = None
    #     else:
    #         input_date = input_date.replace("-","")
    #     self.input_date = input_date
    #     return input_date    
    
    # def set_default_start_date(self, start_date):
    #     start_date = DATE_GENESIS.replace("-","") if self.input_date == None else self.input_date
    #     return start_date
    
    # def set_default_end_date(self, end_date):
    #     end_date = get_yesterday().replace("-","") if self.input_date == None else self.input_date
    #     return end_date
    
    
    # def set_file_folder(self, file_folder=None):
    #     file_folder_default = f'dataset-menu{self.menu_code}' if file_folder == None else f'dataset-save{get_today(form="yyyymmdd")}'
    #     if self.fund_code=='' and self.menu_code in menu_codes_snapshot:
    #         file_folder_default = f'dataset-menu{self.menu_code}-snapshot'
        
    #     file_folder_path = os.path.join(BASE_FOLDER_PATH, file_folder_default) if file_folder == None else file_folder  
    #     check_folder_and_create_folder(file_folder_path)
    #     self.file_folder = file_folder_path
    #     return file_folder_path
    

    # def set_file_name(self, file_name=None):
    #     fund_code_value = '000000' if self.fund_code == '' else self.fund_code
    #     self.file_name_timeseries = f'menu{self.menu_code}-code{fund_code_value}-from{self.start_date}-to{self.end_date}-save{get_today(form="yyyymmdd")}.csv'
    #     self.file_name_snapshot = f'menu{self.menu_code}-code{fund_code_value}-at{self.end_date}-save{get_today(form="yyyymmdd")}.csv'
    #     self.file_name_period = f'menu{self.menu_code}-code{fund_code_value}-between{self.start_date}-and{self.end_date}-save{get_today(form="yyyymmdd")}.csv'

    #     if not self.input_date and self.menu_code:
    #         file_name = self.file_name_timeseries
    #     elif self.menu_code in menu_codes_period:
    #         file_name = self.file_name_period

    #     if self.input_date:
    #         file_name = self.file_name_snapshot
 
    #     if file_name is not None:
    #         file_name = file_name

    #     self.file_name = file_name
    #     return file_name
    

    # def set_bucket_prefix(self):
    #     bucket_prefix = self.file_folder_name
    #     self.bucket_prefix = bucket_prefix
    #     return bucket_prefix

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
        print(f'| (step) open menu: {self.menu_code}')
        coord = self.get_coord_of_sequence('input_menu_code')
        execute_input_menu_code_of_menu_and_enter(coord_input_menu=coord, menu_code=self.menu_code)
        return None
    
    def execute_input_fund_code(self):
        fund_code_value = 'all funds' if self.fund_code == '' else self.fund_code
        print(f'| (step) input fund code: {fund_code_value}')
        coord = self.get_coord_of_sequence('input_fund_code')
        execute_input_fund_code(coord_input_fund_code=coord, fund_code=self.fund_code)
        wait_for_n_seconds(1)
        return None
    
    def execute_input_start_date(self):
        print(f'| (step) input start date: {self.start_date}')
        coord = self.get_coord_of_sequence('input_start_date')
        input_something_on_input_field(coord_input=coord, something=self.start_date)
        return None
    
    def execute_input_end_date(self):
        print(f'| (step) input end date: {self.end_date}')
        coord = self.get_coord_of_sequence('input_end_date')
        input_something_on_input_field(coord_input=coord, something=self.end_date)
        return None
    
    def execute_input_ref_date(self):
        print(f'| (step) input ref date: {self.input_date}')
        coord = self.get_coord_of_sequence('input_ref_date')
        input_something_on_input_field(coord_input=coord, something=self.input_date)
        wait_for_n_seconds(1)
        return None
    
    def execute_button_search(self):
        print(f'| (step) click search button')
        coord = self.get_coord_of_sequence('button_search')
        click_button(coord_button=coord)
        if not is_now_search_loading():
            pass
        wait_for_n_seconds(3)
        return None

    def execute_button_excel(self):
        print(f'| (step) click excel button')
        coord = self.get_coord_of_sequence('button_excel')
        mapping = self.mapping_sequence_to_coordinate
        click_button(coord_button=coord)
        if 'button_excel_popup' not in mapping.keys():
            if not is_now_data_loading():
                pass
            wait_for_n_seconds(3)
        return None

    def execute_button_excel_popup(self):
        print(f'| (step) click excel popup button')
        coord = self.get_coord_of_sequence('button_excel_popup')
        click_button(coord_button=coord)
        # if self.menu_code in menu_codes_having_fast_excel_execution and is_on_running_excel():
        #     return None
        if is_data_loading_started():
            pass
        if not is_now_data_loading():
            pass
        wait_for_n_seconds(3)
        return None

    def execute_button_tab_category(self):
        print(f'| (step) click tab category button')
        coord = self.get_coord_of_sequence('button_tab_category')
        click_button(coord_button=coord)
        wait_for_n_seconds(3)
        return None

    def execute_button_dropdown_period(self):
        print(f'| (step) click dropdown input for period')
        coord = self.get_coord_of_sequence('button_dropdown_period')
        click_button(coord_button=coord)
        wait_for_n_seconds(1)
        return None
    
    def execute_button_select_alldays(self):
        print(f'| (step) click select alldays button')
        coord = self.get_coord_of_sequence('button_select_alldays')
        click_button(coord_button=coord)
        wait_for_n_seconds(1)
        return None

    def execute_cancel_no_data_popup(self):
        print(f'| (step) cancel no data popup')
        if is_there_no_data_popup():
            press('esc')
        wait_for_n_seconds(3)
        return None

    def execute_process_on_excel(self):  
        control_on_excel_to_save_as_popup()
        control_on_save_as_popup(file_folder=self.file_folder, file_name=self.file_name)
        wait_for_n_seconds(3)
        close_excel()
        wait_for_n_seconds(2)
        FUND_CODES_EXCEPTION_FOR_MENU2160 = ['100180', '100181', '100182', '100183']
        exception = True if self.menu_code in menu_codes_validate_exception else False
        if validate_download_process(self.file_folder, self.file_name, exception=exception):
            upload_downloaded_dataset_to_s3(self.file_folder, self.file_name, bucket_prefix=self.bucket_prefix)
        elif self.fund_code in FUND_CODES_EXCEPTION_FOR_MENU2160:
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
            'button_tab_category': self.execute_button_tab_category,
            'button_dropdown_period': self.execute_button_dropdown_period,
            'button_select_alldays': self.execute_button_select_alldays,
        }
        return mapping_sequence[sequence]()
    
    def execute_all_sequences(self):
        if not hasattr(self, 'sequences'):
            self.get_sequences()
        for sequence in self.sequences:
            self.execute_sequence(sequence)
            if self.menu_code == '4604' and sequence == 'button_search':
                self.execute_cancel_no_data_popup()
        self.execute_process_on_excel()
        return None
    
    def recursive_download_dataset(self):
        print(f'⏳ download start: {self.file_name} in {self.file_folder}')
        if is_dataset_downloaded(fund_code=self.file_folder, save_file_folder=self.file_folder, file_name=self.file_name):
            print(f'⭕ download complete: {self.file_name} in {self.file_folder}')
        else:
            self.execute_all_sequences()
            self.recursive_download_dataset()
        return None
    


def get_df_coordinate_of_menu(menu_code):
    df = open_recorded_coordinates(file_folder=COORDINATE_FOLDER, subject=f'menu{menu_code}')
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


def set_dates_by_initial_inputs(input_date, start_date, end_date, menu_code):
    if input_date:
        input_date = input_date
        start_date = input_date
        end_date = input_date
    else:
        if start_date != None and end_date != None and start_date == end_date:
            input_date = end_date
            start_date = end_date
            end_date = end_date
        elif start_date != None and end_date != None and start_date != end_date:
            input_date = None
            start_date = start_date
            end_date = end_date
        elif start_date != None and end_date == None:
            input_date = None
            start_date = start_date
            end_date = get_yesterday()
        elif start_date == None and end_date != None:
            input_date = None
            start_date = DATE_GENESIS
            end_date = end_date
        elif start_date == None and end_date == None and menu_code in MENU_CODES_SNAPSHOT:
            input_date = get_yesterday()
            start_date = None
            end_date = None
        else: 
            input_date = None
            start_date = DATE_GENESIS
            end_date = get_yesterday() 

    input_date = input_date.replace('-', '') if input_date != None else None
    start_date = start_date.replace('-', '') if start_date != None else None
    end_date = end_date.replace('-', '') if end_date != None else None

    dct_dates = {
        'input_date': input_date,
        'start_date': start_date,
        'end_date': end_date
    }

    return dct_dates


def set_file_folder(menu_code, fund_code):
    if menu_code in MENU_CODES_TIMESERIES_BUT_SNAPSHOT and fund_code == '':
        file_folder = f'dataset-menu{menu_code}-snapshot'
    elif menu_code in MENU_CODES_SNAPSHOT and fund_code == '':
        file_folder = f'dataset-menu{menu_code}-snapshot'
    else:
        file_folder = f'dataset-menu{menu_code}'
    return file_folder
