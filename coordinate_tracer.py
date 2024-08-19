import pyautogui
from pynput import mouse, keyboard
import time
import os
import pandas as pd
from shining_pebbles import *

class Tracer:
    def __init__(self, subject):
        self.subject = subject
        self.file_folder = check_folder_and_create_folder('dataset-coordinate')
        self.file_name = f'dataset-coordinate-{subject}-save{get_today("%Y%m%d%H")}.csv'

    def record_coordinates(self):
        data = get_multiple_click_coordinates(timeout=20)
        df = pd.DataFrame(data)
        df.index = range(1, len(df)+1)
        df.index.name = 'step'
        df.columns.name = self.subject
        df.to_csv(os.path.join(self.file_folder, self.file_name), encoding='utf-8-sig')
        print(f"📄 Recorded coordinates saved to {self.file_name}")
        return df

    def import_recorded_coordinates(self):
        df = open_recorded_coordinates(file_folder=self.file_folder, subject=self.subject)
        self.recorded_coordinates = df
        return df
    
    def append_sequences_to_recorded_coordinates(self, sequences):
        if not hasattr(self, 'recorded_coordinates'):
            self.import_recorded_coordinates()
        df = self.recorded_coordinates
        df['sequence'] = sequences
        df.to_csv(os.path.join(self.file_folder, self.file_name), encoding='utf-8-sig')
        print(f"📄 Sequences appended to {self.file_name}")
        return df

def create_click_handlers(screen_width, screen_height, click_data_list, is_single_click=False):
    last_movement_time = time.time()
    is_running = True

    def on_click(x, y, button, pressed):  # 'button' 인수 추가
        nonlocal last_movement_time
        if pressed:
            abs_x, abs_y = x, y
            rel_x, rel_y = round(x/screen_width, 4), round(y/screen_height, 4)
            click_data = {
                'screen_size': (screen_width, screen_height),
                'absolute_coord': (abs_x, abs_y),
                'relative_coord': (rel_x, rel_y)
            }
            click_data_list.append(click_data)
            print(f'Clicked at ({abs_x}, {abs_y})')
            last_movement_time = time.time()
            if is_single_click:
                return False 

    def on_move(x, y):  # 'x'와 'y' 인수 추가
        nonlocal last_movement_time
        last_movement_time = time.time()

    def on_press(key):
        nonlocal is_running
        if key == keyboard.Key.esc:
            is_running = False
            return False  

    return on_click, on_move, on_press, lambda: is_running, lambda: last_movement_time

def get_single_click_coordinates():
    screen_width, screen_height = pyautogui.size()
    click_data_list = []

    on_click, _, on_press, is_running, _ = create_click_handlers(screen_width, screen_height, click_data_list, True)

    print("화면의 아무 곳이나 클릭하세요. ESC를 누르면 종료됩니다.")

    with mouse.Listener(on_click=on_click) as mouse_listener, keyboard.Listener(on_press=on_press) as keyboard_listener:
        while is_running() and not click_data_list:
            pass

    return click_data_list[0] if click_data_list else None


def get_multiple_click_coordinates(timeout=20):
    screen_width, screen_height = pyautogui.size()
    click_data_list = []

    on_click, on_move, on_press, is_running, get_last_movement_time = create_click_handlers(screen_width, screen_height, click_data_list)

    print(f"화면을 클릭하세요. {timeout}초간 움직임이 없거나 ESC를 누르면 종료됩니다.")

    with mouse.Listener(on_click=on_click, on_move=on_move) as mouse_listener, keyboard.Listener(on_press=on_press) as keyboard_listener:
        while is_running():
            if time.time() - get_last_movement_time() > timeout:
                print(f"{timeout}초간 움직임이 없어 종료합니다.")
                break
            time.sleep(0.1)  

    return click_data_list


def open_recorded_coordinates(file_folder, subject):
    df = open_df_in_file_folder_by_regex(file_folder=file_folder, regex=subject)
    cols = df.columns
    for i, col in enumerate(cols):
        if i in [0, 1]:
            df[col] = df[col].apply(lambda x:str_to_tuple(x))
        elif i in [2]:
            df[col] = df[col].apply(lambda x:str_to_float_tuple(x))
        else: 
            pass
    return df


def str_to_tuple(s):
    numbers = s.strip('()').split(',')
    return tuple(map(int, numbers))


def str_to_float_tuple(s):
    numbers = s.strip('()').split(',')
    return tuple(map(float, numbers))

