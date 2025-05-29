from mongodb_controller import COLLECTION_2206
from database_managing import Menu2206s
from database_managing.insert_applications.s3_application import upload_nonexisting_menu_files_to_bucket

upload_nonexisting_menu_files_to_bucket(menu_code='2206')

m = Menu2206s()
m.fetch_snapshots()
m.insert_all()

dates_db = COLLECTION_2206.distinct('일자')[::-1][:10]
print(dates_db)
