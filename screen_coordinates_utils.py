import cv2
import numpy as np
import mss
import time
import pyautogui
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
        print(f"Waiting for {n} seconds...")
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
        raise FileNotFoundError(f"Image file '{image_path}' not found.")

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
        print(f"Cursor moved to coordinates: ({center_x}, {center_y})")
    else:
        print("Image not found on the screen.")

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
        print(f"Clicked at coordinates: ({center_x}, {center_y})")
    else:
        print("Image not found on the screen.")


def check_image_appearance(image_path, max_check_time=30, check_interval=1):
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
        raise FileNotFoundError(f"-- Image file '{image_path}' not found.")
    
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
            print("-- Image found on the screen. Returning True.")
            return True

        elapsed_time = time.time() - start_time
        if elapsed_time > max_check_time:
            print("-- Maximum check time exceeded. Stopping check. Assume it does not exist.")
            return False

        time.sleep(check_interval)


def check_image_disappearance(image_path, max_check_time=30, check_interval=1):
    """
    Continuously checks if the given image disappears from the screen within the maximum check time.

    Args:
        image_path (str): Path to the image file.
        max_check_time (int): Maximum time in seconds to check for the image. Defaults to 30.
        check_interval (int): Interval in seconds between each check. Defaults to 1.

    Returns:
        bool: False if the image disappears, True if the maximum check time is exceeded.
    """
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Image file '{image_path}' not found.")
    
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
            print("-- Image found on the screen. Continuing to check...")
        else:
            print("-- Image not found on the screen. Returning True.")
            return True

        elapsed_time = time.time() - start_time
        if elapsed_time > max_check_time:
            print("-- Maximum check time exceeded. Stopping check. Assume it does not exist")
            return True

        time.sleep(check_interval)


def check_image_birth_and_death(image_path, max_check_time_appear=3, max_check_time_disappear=10):
    birth = check_image_appearance(image_path, max_check_time=max_check_time_appear)
    if birth:
        print('- Image appeared')
        death = check_image_disappearance(image_path, max_check_time=max_check_time_disappear)
        print('- Image disappeared')
    else:
        print('- Image has not appeared')
        death = True
    return birth, death


def type_string(input_string):
    """
    Types the given string using the keyboard.

    Args:
        input_string (str): The string to be typed.
    """
    pyautogui.typewrite(input_string)
    print(f"Typed string: {input_string}")


def press_enter():
    """
    Presses the Enter key.
    """
    pyautogui.press('enter')
    print("Pressed Enter key.")


def press_esc():
    """
    Presses the ESC key.
    """
    pyautogui.press('esc')
    print("Pressed ESC key.")


def press_key(key):
    """
    Presses the a key.
    """
    pyautogui.press(key)
    print(f"Pressed '{key}' key.")




def move_cursor_to(x, y):
    pyautogui.moveTo(x, y)
    print(f"Cursor moved to coordinates: ({x}, {y})")



def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y})")
        # 클릭 후 바로 리스너를 멈추려면 아래 줄을 추가합니다.
        return False


def get_click_coordinates():
    # 마우스 클릭 리스너를 시작합니다.
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
    print(f"Clicked at coordinates: ({x}, {y})")
