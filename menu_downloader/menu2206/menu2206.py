import os
from shining_pebbles import get_yesterday, get_today
from menu_downloader.coordinate_utils import ( 
    load_menu_coordinates,
    get_coordinates_of_menu, 
    get_sequences_of_menu
)
from menu_downloader.coordinate_utils import (
    get_mapping_sequences_to_coordinates
)
from menu_downloader.consts import (
    DATALAKE_DIR,
    FILE_FOLDER,
    FUND_CODE_DEFAULT,
    BUCKET,
    BUCKET_PREFIX,
    MAPPING_MENU_CODE_INPUT,
    FILE_NAME_FORMAT
)
from menu_downloader.screen_controller import (
    wait_for_n_seconds,
    click_button,
    input_something_on_input_field
)
from menu_downloader.menu_controller import (
    execute_input_menu_code_and_press_enter,
    is_now_search_loading,
)
from .menu2206_time_consts import (
    TIME_INTERVAL_BETWWEN_SEQUENCES,
    TIME_INTERVAL_BETWWEN_SEQUENCES_LONG,
    TIME_INTERVAL_BETWWEN_SEQUENCES_SHORT
)

class MOS2206:
    def __init__(self, menu_code='2206', date_ref=None):
        self.menu_code = menu_code
        self.menu_code_input = MAPPING_MENU_CODE_INPUT.get(menu_code, menu_code)
        self.fund_code = FUND_CODE_DEFAULT
        self.date_ref = self.set_date_ref(date_ref) 
        self.file_folder = self.set_file_folder()
        self.folder_path = self.set_folder_path()
        self.file_name = self.set_file_name()
        self.file_path = self.set_file_path()
        self.bucket = BUCKET
        self.bucket_prefix = self.set_bucket_prefix()
        self.df_coordinates = self.get_df_coordinats()
        self.coordinates = self.get_coordinates()
        self.sequences = self.get_sequences()
        self.mapping_sequences = self.get_mapping_sequences()

    def set_date_ref(self, date_ref):
        self.date_ref = date_ref if date_ref else get_yesterday()
        self.date_ref_nondashed = self.date_ref.replace('-', '')
        self.today = get_today()
        self.today_nondashed = self.today.replace('-', '')
        return self.date_ref

    def set_file_folder(self):
        return self.get_value(FILE_FOLDER, self.menu_code)

    def set_folder_path(self):
        return os.path.join(DATALAKE_DIR, self.file_folder)
 
    def set_file_name(self):
        return self.get_value(FILE_NAME_FORMAT, self.menu_code, self.fund_code, self.date_ref_nondashed, self.today_nondashed)

    def set_file_path(self):
        return os.path.join(self.folder_path, self.file_name)

    def set_bucket_prefix(self):
        return self.get_value(BUCKET_PREFIX, self.menu_code)

    def get_df_coordinats(self):
        return load_menu_coordinates(self.menu_code)
    
    def get_coordinates(self):
        return get_coordinates_of_menu(self.menu_code)
    
    def get_sequences(self):
        return get_sequences_of_menu(self.menu_code)
    
    def get_mapping_sequences(self):
        return get_mapping_sequences_to_coordinates(self.df_coordinates)
    
    def execute_input_menu_code(self):
        wait_for_n_seconds(TIME_INTERVAL_BETWWEN_SEQUENCES)
        print(f'| (step) open menu: {self.menu_code}')
        coord = self.mapping_sequences['input_menu_code']
        execute_input_menu_code_and_press_enter(coord_input_menu=coord, menu_code=self.menu_code_input)
        return None
  
    def execute_button_tab_category(self):
        wait_for_n_seconds(TIME_INTERVAL_BETWWEN_SEQUENCES)
        print(f'| (step) click tab category button')
        coord = self.mapping_sequences['button_tab_category']
        click_button(coord_button=coord)
        return None

    def execute_input_fund_code(self):
        fund_code_to_input = '' if self.fund_code == FUND_CODE_DEFAULT else self.fund_code
        if self.fund_code == FUND_CODE_DEFAULT:
            print(f'| (step) input fund code: ALL_FUNDS')
        else:
            print(f'| (step) input fund code: {self.fund_code}')
        coord = self.mapping_sequences['input_fund_code']
        input_something_on_input_field(coord_input_fund_code=coord, fund_code=fund_code_to_input)
        return None
    
    def execute_input_date_ref(self):
        print(f'| (step) input ref date: {self.date_ref}')
        coord = self.mapping_sequences['input_ref_date']
        input_something_on_input_field(coord_input=coord, something=self.date_ref_nondashed)
        return None
    
    def execute_button_search(self):
        print(f'| (step) click search button')
        coord = self.mapping_sequences['button_search']
        click_button(coord_button=coord)
        if not is_now_search_loading():
            pass
        wait_for_n_seconds(3)
        return None

    def execute_button_excel(self):
        print(f'| (step) click excel button')
        coord = self.mapping_sequences['button_excel']
        mapping = self.mapping_sequence_to_coordinate
        click_button(coord_button=coord)
        if 'button_excel_popup' not in mapping.keys():
            if not is_now_data_loading():
                pass
            wait_for_n_seconds(3)
        return None

    def execute_button_excel_popup(self):
        print(f'| (step) click excel popup button')
        coord = self.mapping_sequences['button_excel_popup']
        click_button(coord_button=coord)
        # if self.menu_code in menu_codes_having_fast_excel_execution and is_on_running_excel():
        #     return None
        if is_data_loading_started():
            pass
        if not is_now_data_loading():
            pass
        wait_for_n_seconds(3)
        return None


    def execute_sequence(self, sequence):
        mapping_executions = {
            'input_menu_code': self.execute_input_menu_code,
            'button_tab_category': self.execute_button_tab_category,
        }
        return mapping_executions[sequence]()
    
    def execute_all_sequences(self, option_verbose=False):
        if not hasattr(self, 'sequences'):
            self.get_sequences()
        for i, sequence in enumerate(self.sequences):
            if option_verbose:
                print(f'| (step) {i+1}/{len(self.sequences)}: {sequence}')
            self.execute_sequence(sequence)
        # self.execute_process_on_excel()
        return None    
        

    @staticmethod
    def get_value(value, *args):
        if callable(value):
            return value(*args)
        return value
    

    
