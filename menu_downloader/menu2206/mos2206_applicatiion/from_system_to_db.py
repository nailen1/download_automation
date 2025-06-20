from menu_downloader.menu2206 import MOS2206
from menu_downloader.screen_controller import wait_for_n_seconds
from database_managing.insert_applications.s3_application import upload_nonexisting_menu_files_to_bucket
from database_managing.insert_utils import Menu2206s


def download_and_upload_and_insert_menu2206(date_ref):
    mos = MOS2206(date_ref=date_ref)
    mos.execute_all_sequences()
    wait_for_n_seconds(5)

    upload_nonexisting_menu_files_to_bucket(menu_code='2206')

    m = Menu2206s()
    m.fetch_snapshots()
    m.insert_all()