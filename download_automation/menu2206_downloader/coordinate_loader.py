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
    for i, col in enumerate(cols):
        if i in [0, 1]:
            df[col] = df[col].apply(lambda x:str_to_tuple(x))
        elif i in [2]:
            df[col] = df[col].apply(lambda x:str_to_float_tuple(x))
        else: 
            pass
    return df

def load_menu_coordinates(menu_code):
    regex = f'dataset-coordinate-menu{menu_code}'
    df = load_csv_in_file_folder_by_regex(file_folder=FILE_FOLDER_COORDINATE, regex=regex)
    return df

def get_sequences_of_menu(menu_code):
    df = load_menu_coordinates(menu_code)
    sequences = list(df['sequence'])
    return sequences

def get_coordinates_of_menu(menu_code, coord_type='absolute_coord'):
    # df = load_menu_coordinates(menu_code)
    df = (
        menu_code
        .pipe(load_menu_coordinates)
        .pipe(preprocess_recorded_coordinates)
    )
    coordinates = list(df[coord_type])
    return coordinates