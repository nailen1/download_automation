from pyautogui import (
    click,
    hotkey, 
    press, 
    typewrite
)
from .screen_basis import (
    wait_for_n_seconds,
)
from .screen_time_consts import (
    TIME_INTERVAL_BETWWEN_CLICK_AND_KEYBOARD_CONTOL,
    TIME_INTERVAL_BETWWEN_KEYBOARD_CONTOLS,
    TIME_INTERVAL_BETWWEN_KEYBOARD_CONTOL_AND_TYPING,
)

def input_something_on_input_field(coord_input, something, verbose=False):
    if verbose:
        print(f'- input {something} on {coord_input}')
    click(coord_input)
    wait_for_n_seconds(TIME_INTERVAL_BETWWEN_CLICK_AND_KEYBOARD_CONTOL)
    hotkey('ctrl', 'a')
    wait_for_n_seconds(TIME_INTERVAL_BETWWEN_KEYBOARD_CONTOLS)
    press('backspace')
    wait_for_n_seconds(TIME_INTERVAL_BETWWEN_KEYBOARD_CONTOL_AND_TYPING)
    typewrite(list(something))
    return None

def click_button(coord_button, verbose=False):
    if verbose:
        print(f'- click button')
    click(coord_button)
    return None

