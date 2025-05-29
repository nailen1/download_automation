from pyautogui import press, move
from menu_downloader.screen_controller import input_something_on_input_field, wait_for_n_seconds
from menu_downloader.screen_controller import click_button
from .menu_time_consts import TIME_INTERVAL_BETWWEN_TYPING_AND_ENTER

def execute_input_menu_code_and_press_enter(coord_input_menu, menu_code):
    input_something_on_input_field(coord_input=coord_input_menu, something=menu_code)
    wait_for_n_seconds(TIME_INTERVAL_BETWWEN_TYPING_AND_ENTER)
    press('enter')
    return None

def close_menu_window(coord_close_menu):
    move(coord_close_menu)
    wait_for_n_seconds(1)
    click_button(coord_button=coord_close_menu)
    return None