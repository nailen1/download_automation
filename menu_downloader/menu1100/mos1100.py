import os
from menu_downloader.menu2206.mos2206 import MOS2206
from menu_downloader.screen_controller import (
    wait_for_n_seconds,
    input_something_on_input_field,
    click_button
)
from menu_downloader.consts import (
    MAPPING_MENU_CODE_INPUT,
    FILE_FOLDER,
    DATALAKE_DIR,
    SNAPSHOT_FILE_NAME_FORMAT,
    TIMESERIES_FILE_NAME_FORMAT,
    BUCKET_PREFIX
)
from menu_downloader.menu_controller.menu_time_consts import (
    TIME_INTERVAL_BETWEEN_SEQUENCES,
    TIME_INTERVAL_BETWEEN_SEQUENCES_SHORT
)
from string_date_controller import (
    get_yesterday,
)
from .mos1100_consts import MAPPING_PSEUDO_CODES
from menu_downloader.excel_controller import (
    is_dataset_downloaded,
)

class MOS1100(MOS2206):
    def __init__(self, menu_code='1100', start_date=None, end_date=None, date_ref=None):
        self.start_date = self.set_start_date(start_date=start_date)
        self.end_date = self.set_end_date(end_date=end_date)
        super().__init__(menu_code=menu_code, date_ref=date_ref, fund_code=MAPPING_PSEUDO_CODES[menu_code])
        self.file_folder = self.set_file_folder()
        self.folder_path = self.set_folder_path()
        self.file_name = self.set_file_name()
        self.file_path = self.set_file_path()
        self.bucket_prefix = self.set_bucket_prefix()

    def set_start_date(self, start_date):
        self.start_date = start_date if start_date else get_yesterday()
        self.start_date_nondashed = self.start_date.replace("-","")
        return self.start_date
    
    def set_end_date(self, end_date):
        self.end_date = end_date if end_date else get_yesterday()
        self.end_date_nondashed = self.end_date.replace("-","")
        return self.end_date

    def set_file_folder(self, folder_label=None):
        folder_label = folder_label if folder_label else self.menu_code_input
        return self.get_value(FILE_FOLDER, folder_label)
 
    def set_folder_path(self):
        return os.path.join(DATALAKE_DIR, self.file_folder)

    def set_file_path(self):
        return os.path.join(self.folder_path, self.file_name)

    def set_file_name(self, name_label=None):
        name_label = name_label if name_label else self.menu_code_input
        if self.start_date < self.end_date:
            file_name = self.get_value(TIMESERIES_FILE_NAME_FORMAT, name_label, self.fund_code, self.start_date_nondashed, self.end_date_nondashed, self.today_nondashed)
        elif self.start_date == self.end_date:
            file_name = self.get_value(SNAPSHOT_FILE_NAME_FORMAT, name_label, self.fund_code, self.end_date_nondashed, self.today_nondashed)
        return file_name

    def set_bucket_prefix(self):
        return self.get_value(BUCKET_PREFIX, self.menu_code_input)

    def execute_input_date(self, date_label):
        mapping_date_label = {
            'ref_date': self.date_ref,
            'start_date': self.start_date,
            'end_date': self.end_date
        }
        wait_for_n_seconds(TIME_INTERVAL_BETWEEN_SEQUENCES)
        print(f'| (step) input {date_label} date: {mapping_date_label[date_label]}')
        coord = self.mapping_sequences[f'input_{date_label}']
        input_something_on_input_field(coord_input=coord, something=mapping_date_label[date_label].replace('-', ''))
        return None

    execute_input_start_date = lambda self: self.execute_input_date('start_date')
    execute_input_end_date = lambda self: self.execute_input_date('end_date')

    def execute_check(self, checkbox_index):
        wait_for_n_seconds(TIME_INTERVAL_BETWEEN_SEQUENCES_SHORT)
        print(f'| (step) click checkbox')
        coord = self.mapping_sequences[f'check_{checkbox_index}']
        click_button(coord_button=coord)
        wait_for_n_seconds(TIME_INTERVAL_BETWEEN_SEQUENCES_SHORT)
        return None

    execute_check_1 = lambda self: self.execute_check(1)
    execute_check_2 = lambda self: self.execute_check(2)
    execute_check_3 = lambda self: self.execute_check(3)
    execute_check_4 = lambda self: self.execute_check(4)
    execute_check_5 = lambda self: self.execute_check(5)


    def execute_sequence(self, sequence):
        mapping_executions = {
            'input_menu_code': self.execute_input_menu_code,
            'button_tab_category': self.execute_button_tab_category,
            'input_fund_code': self.execute_input_fund_code,
            'input_ref_date': self.execute_input_date_ref,
            'input_start_date': self.execute_input_start_date,
            'input_end_date': self.execute_input_end_date,
            'button_search': self.execute_button_search,
            'button_excel': self.execute_button_excel,
            'button_excel_popup': self.execute_button_excel_popup,
            'check_1': self.execute_check_1,
            'check_2': self.execute_check_2,
            'check_3': self.execute_check_3,
            'check_4': self.execute_check_4,
            'check_5': self.execute_check_5,
        }
        return mapping_executions[sequence]()
    