# screen_control_utils.py

import cv2
import numpy as np
import mss
import time
import pyautogui
from pynput import mouse
from typing import List, Dict, Optional, Tuple

def wait_for_n_seconds(n: int, verbose: bool = False) -> None:
    if verbose:
        print(f"____waiting for {n} seconds...")
    time.sleep(n)
    return None


def check_image_appearance(image_path, max_check_time=30, check_interval=1, option_verbose=False):
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"____image file '{image_path}' not found.")
    
    start_time = time.time()
    
    while True:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            screenshot = np.array(screenshot)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.8)

        if len(loc[0]) > 0:
            if option_verbose:
                print("____image found on the screen. returning true.")
            return True

        elapsed_time = time.time() - start_time
        if elapsed_time > max_check_time:
            if option_verbose:
                print("____maximum check time exceeded. stopping check. assume it does not exist.")
            return False

        wait_for_n_seconds(check_interval)