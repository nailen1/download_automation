import os
import pandas as pd
from shining_pebbles import scan_files_including_regex, load_csv_in_file_folder_by_regex
from aws_s3_controller import scan_files_in_bucket_by_regex, open_df_in_bucket_by_regex
from mongodb_controller import client
from string_date_controller import map_date_nondashed_to_dashed
from menu_downloader.consts import DATALAKE_DIR
import shutil

class TDP:
    def __init__(self, file_name, folder_path):
        self.file_name = file_name
        self.folder_path = folder_path

    def parse_file_name(self):
        self.menu_code = self.file_name.split('menu')[-1].split('-code')[0]
        self.fund_code = self.file_name.split('-code')[-1].split('-at')[1].split('.')[0]
        if '-at' in self.file_name: 
            self.date_ref = map_date_nondashed_to_dashed(self.file_name.split('-at')[-1].split('-save')[0])
        elif '-from' in self.file_name and '-to' in self.file_name:
            self.start_date = map_date_nondashed_to_dashed(self.file_name.split('from')[-1].split('-to')[0])
            self.end_date = map_date_nondashed_to_dashed(self.file_name.split('to')[-1].split('-save')[0])
        elif '-between' in self.file_name and '-and' in self.file_name:
            self.start_date = map_date_nondashed_to_dashed(self.file_name.split('between')[-1].split('-and')[0])
            self.end_date = map_date_nondashed_to_dashed(self.file_name.split('and')[-1].split('-save')[0])
        self.date_save = map_date_nondashed_to_dashed(self.file_name.split('-save')[-1].split('.')[0])


    def scan_local(self):
        try:
            self.file_name_local = scan_files_including_regex(file_folder=self.folder_path, regex=self.file_name)[-1]
            return self.file_name_local
        except Exception:
            print(f'File {self.file_name} not found in {self.folder_path}.')
    
    def load_local(self):
        self.df_local = load_csv_in_file_folder_by_regex(file_folder=self.folder_path, regex=self.file_name_local)
        return self.df_local

    def validate_local(self):
        print(f'📂 Validating local')
        try:
            self.parse_file_name()
            self.scan_local()
            self.load_local()
        except:
            print(f'Error parsing file name {self.file_name} or loading local data.')
            return False
        if self.file_name_local is None:
            print(f'File {self.file_name} not found in {self.folder_path}.')
            return False
        if self.df_local.empty:
            print(f'File {self.file_name_local} is empty.')
            return False
        if len(self.df_local) < 2:
            print(f'File {self.file_name_local} has no valid data.')
            return False
        print(f'File {self.file_name_local} is valid with {len(self.df_local)} rows.')
        return True

    def scan_db(self):
        collection = client['database-rpa'][f'dataset-menu{self.menu_code}']
        pipeline = [
            {
                '$match': {
                    '일자': self.date_ref,
                }
            },
            {
                '$project': {
                    '_id': 0,
                    '일자': 1,
                    '펀드코드': 1,
                    '펀드명': 1,
                }
            }
        ]
        cursor = collection.aggregate(pipeline)
        self.data_db = list(cursor)
        return self.data_db
    
    def load_db(self):
        self.df_db = pd.DataFrame(self.scan_db())
        return self.df_db

    def validate_db(self):
        print(f'📦 Validating database')
        try:
            self.scan_db()
            self.load_db()
        except Exception as e:
            print(f'Error scanning or loading database: {e}')
            return False
        if self.data_db is None:
            print(f'No data found in database for menu {self.menu_code} on date {self.date_ref}.')
            return False
        if self.df_db.empty:
            print(f'No data found in database for menu {self.menu_code} on date {self.date_ref}.')
            return False
        if len(self.df_db) < 2:
            print(f'Database has no valid data for menu {self.menu_code} on date {self.date_ref}.')
            return False
        print(f'Database has {len(self.df_db)} records for menu {self.menu_code} on date {self.date_ref}.')
        return True

    def scan_s3(self):
        try:
            self.file_name_s3 = scan_files_in_bucket_by_regex(bucket='dataset-system', bucket_prefix=f'dataset-menu{self.menu_code}', regex=self.file_name)[-1]
            return self.file_name_s3
        except Exception:
            print(f'File {self.file_name} not found in S3 bucket.')

    def load_s3(self):
        self.df_s3 = open_df_in_bucket_by_regex(bucket='dataset-system', bucket_prefix=f'dataset-menu{self.menu_code}', regex=self.file_name_s3)
        return self.df_s3

    def validate_s3(self):
        print(f'🪣 Validating S3')
        try:
            self.scan_s3()
            self.load_s3()
        except Exception as e:
            print(f'Error scanning or loading S3 data: {e}')
            return False
        if self.df_s3.empty:
            print(f'File {self.file_name_s3} is empty in S3 bucket.')
            return False
        if len(self.df_s3) < 2:
            print(f'File {self.file_name_s3} has no valid data in S3 bucket.')
            return False
        print(f'File {self.file_name_s3} is valid with {len(self.df_s3)} rows in S3 bucket.')
        return True
    
    def validate_all(self):
        self.parse_file_name()
        if not self.validate_local():
            return False
        self.data_db = self.load_db()
        if not self.validate_db():
            return False
        self.file_name_s3 = self.scan_s3()
        if not self.validate_s3():
            return False
        print(f'All validations passed for {self.file_name}.')
        return True
    
    def delete_local(self):
        if not self.validate_local():
            file_path = os.path.join(self.folder_path, self.file_name_local)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f'Local file {self.file_name_local} deleted.')
            else:
                print(f'Local file {self.file_name_local} does not exist.')
        return None
    
    def move_to_monitoring_local(self) -> bool:
        if not self.validate_local():
            source_file_path = os.path.join(self.folder_path, self.file_name_local)
            archive_folder_path = os.path.join(DATALAKE_DIR, 'dataset-monitoring')
            archive_file_path = os.path.join(archive_folder_path, self.file_name_local)

            os.makedirs(archive_folder_path, exist_ok=True)

            if not os.path.exists(source_file_path):
                print(f'Local file {self.file_name_local} does not exist.')
                return False
            
            try:
                shutil.move(str(source_file_path), str(archive_file_path))
                print(f'Local file {self.file_name_local} archived to {archive_file_path}')
                return True
            except OSError as e:
                print(f'Failed to archive {self.file_name_local}: {e}')
                return False
        
        return False