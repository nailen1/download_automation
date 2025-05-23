import time
import cv2
import numpy as np
import mss
import pyautogui
import logging

logger = logging.getLogger(__name__)


def wait_for_n_seconds(n: int, option_verbose: bool = False) -> None:
    if option_verbose:
        logger.info(f"Waiting for {n} seconds...")
    time.sleep(n)


def load_template(image_path: str) -> np.ndarray:
    """템플릿 이미지를 로드하고 검증합니다."""
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Image file not found: {image_path}")
    return template


def capture_screenshot() -> np.ndarray:
    """현재 화면의 스크린샷을 캡처합니다."""
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
    return screenshot


def match_template(screenshot: np.ndarray, template: np.ndarray, threshold: float = 0.8) -> tuple:
    """템플릿 매칭을 수행하고 결과를 반환합니다."""
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    return loc, result


def is_timeout(start_time: float, timeout: int) -> bool:
    """타임아웃 여부를 확인합니다."""
    return time.time() - start_time > timeout


def wait_until_image_appears(
    image_path: str, 
    timeout: int = 30, 
    check_interval: int = 1, 
    threshold: float = 0.8,
    option_verbose: bool = False
) -> bool:
    template = load_template(image_path)
    start_time = time.time()
    
    while True:
        screenshot = capture_screenshot()
        loc, _ = match_template(screenshot, template, threshold)

        if len(loc[0]) > 0:
            if option_verbose:
                logger.info(f"Image found on screen: {image_path}")
            return True

        if is_timeout(start_time, timeout):
            if option_verbose:
                logger.warning(f"Timeout: Image not found within {timeout} seconds: {image_path}")
            return False

        wait_for_n_seconds(check_interval, option_verbose=False)


def wait_until_image_disappears(
    image_path: str, 
    timeout: int = 30, 
    check_interval: int = 1, 
    threshold: float = 0.8,
    option_verbose: bool = False
) -> bool:
    template = load_template(image_path)
    start_time = time.time()
    
    while True:
        screenshot = capture_screenshot()
        loc, _ = match_template(screenshot, template, threshold)

        if len(loc[0]) == 0:
            if option_verbose:
                logger.info(f"Image disappeared from screen: {image_path}")
            return True

        if is_timeout(start_time, timeout):
            if option_verbose:
                logger.warning(f"Timeout: Image still present after {timeout} seconds: {image_path}")
            return False

        wait_for_n_seconds(check_interval, option_verbose=False)


def move_to_image(
    image_path: str, 
    confidence: float = 0.7, 
    timeout: int = 10,
    option_verbose: bool = True
) -> bool:
    start_time = time.time()
    
    while True:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if location:
                pyautogui.moveTo(location)
                if option_verbose:
                    logger.info(f"Mouse moved to image location: {image_path}")
                return True
                
        except pyautogui.ImageNotFoundException:
            pass
        except Exception as e:
            logger.error(f"Error while locating image: {e}")
            return False

        if is_timeout(start_time, timeout):
            if option_verbose:
                logger.warning(f"Timeout: Could not find image within {timeout} seconds: {image_path}")
            return False
        
        wait_for_n_seconds(1, option_verbose=False)


def is_image_on_screen(
    image_path: str,
    threshold: float = 0.8,
    option_verbose: bool = False
) -> bool:
    template = load_template(image_path)
    screenshot = capture_screenshot()
    loc, _ = match_template(screenshot, template, threshold)
    
    exists = len(loc[0]) > 0
    if option_verbose:
        logger.info(f"Image {'found' if exists else 'not found'} on screen: {image_path}")
    
    return exists


def wait_for_image_change(
    image_path: str,
    timeout: int = 30,
    check_interval: int = 1,
    threshold: float = 0.8,
    option_verbose: bool = False
) -> bool:
    initial_state = is_image_on_screen(image_path, threshold, False)
    
    if option_verbose:
        logger.info(f"Initial state - Image {'present' if initial_state else 'absent'}: {image_path}")
    
    start_time = time.time()
    
    while True:
        current_state = is_image_on_screen(image_path, threshold, False)
        
        if current_state != initial_state:
            if option_verbose:
                logger.info(f"Image state changed to {'present' if current_state else 'absent'}: {image_path}")
            return True
            
        if is_timeout(start_time, timeout):
            if option_verbose:
                logger.warning(f"Timeout: Image state unchanged after {timeout} seconds: {image_path}")
            return False
            
        wait_for_n_seconds(check_interval, option_verbose=False)
