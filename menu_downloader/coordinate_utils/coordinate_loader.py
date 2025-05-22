from shining_pebbles import load_csv_in_file_folder_by_regex 
from .coordinate_consts import FILE_FOLDER_COORDINATE

def str_to_tuple(s):
    numbers = s.strip('()').split(',')
    return tuple(map(int, numbers))

def str_to_float_tuple(s):
    numbers = s.strip('()').split(',')
    return tuple(map(float, numbers))

def preprocess_recorded_coordinates(df):
    cols = df.columns
    for col in cols:
        if col in ['screen_size', 'absolute_coord']:
            df[col] = df[col].apply(lambda x:str_to_tuple(x))
        elif col in ['relative_coord']:
            df[col] = df[col].apply(lambda x:str_to_float_tuple(x))
        else: 
            pass
    return df

def load_menu_coordinates(menu_code):
    regex = f'dataset-coordinate-menu{menu_code}'
    df = load_csv_in_file_folder_by_regex(file_folder=FILE_FOLDER_COORDINATE, regex=regex)
    df = preprocess_recorded_coordinates(df)
    return df
