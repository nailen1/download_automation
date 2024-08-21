# screen_control_utils.py

import cv2
import numpy as np
import mss
import time
import pyautogui
from pyautogui import click
from pynput import mouse
from typing import List, Dict, Optional, Tuple


def wait_for_n_seconds(n: int, verbose: bool = False) -> None:
    """
    Pauses the execution for n seconds.
    
    Args:
        n (int): Number of seconds to wait.
        verbose (bool): If True, prints a waiting message. Defaults to True.

    Returns:
        None
    """
    if verbose:
        print(f"    waiting for {n} seconds...")
    time.sleep(n)
    return None

def find_image_on_screen(image_path, threshold=0.8):
    """
    Checks if the given image is present on the screen.

    Args:
        image_path (str): Path to the image file.
        threshold (float): Threshold for template matching. Defaults to 0.8.

    Returns:
        bool: True if the image is found, False otherwise.
    """
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"    image file '{image_path}' not found.")

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)

    return len(loc[0]) > 0

def move_cursor_to_image(image_path):
    """
    Moves the cursor to the center of the given image on the screen.

    Args:
        image_path (str): Path to the image file.
    """
    position = find_image_on_screen(image_path)
    if position:
        h, w, _ = cv2.imread(image_path).shape
        center_x = position[0] + w // 2
        center_y = position[1] + h // 2
        pyautogui.moveTo(center_x, center_y)
        print(f"    cursor moved to coordinates: ({center_x}, {center_y})")
    else:
        print("    image not found on the screen.")

  
def move_to_image(image_path, confidence_level=0.8, timeout=10):
    start_time = time.time()
    while True:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence_level)
            if location:
                pyautogui.moveTo(location)
                return True
        except ImageNotFoundException:
            print(f"    could not find the image '{image_path}'. assuming it is not present.")
            return False

        if time.time() - start_time > timeout:
            print(f"    timeout! could not find the image '{image_path}' within {timeout} seconds.")
            return False
        
        time.sleep(1)


def click_on_image(image_path):
    """
    Clicks on the center of the given image on the screen.

    Args:
        image_path (str): Path to the image file.
    """
    position = find_image_on_screen(image_path)
    if position:
        h, w, _ = cv2.imread(image_path).shape
        center_x = position[0] + w // 2
        center_y = position[1] + h // 2
        pyautogui.click(center_x, center_y)
        print(f"    clicked at coordinates: ({center_x}, {center_y})")
    else:
        print("     ismage not found on the screen.")


def check_image_appearance(image_path, max_check_time=30, check_interval=1, verbose=False):
    """
    Continuously checks if the given image appears on the screen within the maximum check time.

    Args:
        image_path (str): Path to the image file.
        max_check_time (int): Maximum time in seconds to check for the image. Defaults to 30.
        check_interval (int): Interval in seconds between each check. Defaults to 1.

    Returns:
        bool: True if the image appears, False if the maximum check time is exceeded.
    """
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"    image file '{image_path}' not found.")
    
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
            if verbose:
                print("    image found on the screen. returning true.")
            return True

        elapsed_time = time.time() - start_time
        if elapsed_time > max_check_time:
            if verbose:
                print("    maximum check time exceeded. stopping check. assume it does not exist.")
            return False

        time.sleep(check_interval)

def check_image_disappearance(image_path, max_check_time=30, check_interval=1, verbose=False):
    """
    Continuously checks if the given image disappears from the screen within the maximum check time.

    Args:
        image_path (str): Path to the image file.
        max_check_time (int): Maximum time in seconds to check for the image. Defaults to 30.
        check_interval (int): Interval in seconds between each check. Defaults to 1.

    Returns:
        bool: True if the image disappears, False if the maximum check time is exceeded.
    """
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"    image file '{image_path}' not found.")
    
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
            if verbose:
                print("    image still on screen. continuing check...")
        else:
            if verbose:
                print("    image no longer on screen. returning true.")
            return True

        elapsed_time = time.time() - start_time
        if elapsed_time > max_check_time:
            print("    max check time reached. assuming image still present.")
            return False

        time.sleep(check_interval)


def check_image_birth_and_death(image_path, max_check_time_appear=3, max_check_time_disappear=10, verbose=False):
    birth = check_image_appearance(image_path, max_check_time=max_check_time_appear)
    if birth:
        if verbose:
            print('    image appeared on screen')
        death = check_image_disappearance(image_path, max_check_time=max_check_time_disappear)
        if verbose:
            print('    image disappeared from screen')
    else:
        if verbose:
            print('    image did not appear within expected time')
        death = True
    return birth, death


def type_string(input_string):
    """
    Types the given string using the keyboard.

    Args:
        input_string (str): The string to be typed.
    """
    pyautogui.typewrite(input_string)
    print(f"    typed: '{input_string}'")


def press_enter():
    """
    Presses the Enter key.
    """
    pyautogui.press('enter')
    print("    pressed: enter key")


def press_esc():
    """
    Presses the ESC key.
    """
    pyautogui.press('esc')
    print("    pressed: esc key")


def press_key(key):
    """
    Presses a specified key.
    """
    pyautogui.press(key)
    print(f"    pressed: '{key}' key")


def move_cursor_to(x, y):
    pyautogui.moveTo(x, y)
    print(f"    moved cursor to: ({x}, {y})")


def on_click(x, y, button, pressed):
    if pressed:
        print(f"    mouse clicked at: ({x}, {y})")
        return False


def get_click_coordinates():
    print("    waiting for mouse click...")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


def click_at_coordinates(x, y):
    """
    Clicks at the specified coordinates on the screen.

    Args:
        x (int): The x-coordinate where the click should occur.
        y (int): The y-coordinate where the click should occur.
    """
    pyautogui.click(x, y)
    print(f"    clicked at: ({x}, {y})")