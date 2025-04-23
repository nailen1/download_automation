from .database_utils import upload_every_bbg_index

def insert_bbg_index_to_database(database_name='database-rpa'):
    """
    Insert Bloomberg index data into the specified database.
    """
    upload_every_bbg_index(database_name=database_name)
    return None