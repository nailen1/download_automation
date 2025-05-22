from .coordinate_loader import load_menu_coordinates

def get_mapping_sequences_to_coordinates(df, coord_type='absolute_coord'):
    dct = df.set_index('sequence')[coord_type].to_dict()
    return dct
def get_sequences_of_menu(menu_code):
    df = load_menu_coordinates(menu_code)
    sequences = list(df['sequence'])
    return sequences

def get_coordinates_of_menu(menu_code, coord_type='absolute_coord'):
    df = load_menu_coordinates(menu_code)
    coordinates = list(df[coord_type])
    return coordinates