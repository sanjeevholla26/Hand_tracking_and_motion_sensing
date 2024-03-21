import pyautogui
import cv2
import numpy as np

def ZoomIn_ZoomOut(distance):
    if distance > 80:
        pyautogui.hotkey('ctrl', '+')
    else:
        pyautogui.hotkey('ctrl', '-')

def MouseLeftClick(temp):
    if temp:
        pyautogui.click()

def MouseRightClick(temp):
    if temp:
        pyautogui.rightClick()

def ScreenShot(temp):
    if temp:
        pyautogui.screenshot()

def CursorMovement(x1, y1, frameR, wCam, wScr, hCam, hScr, smoothening, clocX, clocY, plocX, plocY):
    # 5. Convert Coordinates
    x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
    y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
    # 6. Smoothen Values

    clocX = plocX + (x3 - plocX) / smoothening
    clocY = plocY + (y3 - plocY) / smoothening

    # 7. Move Mouse
    pyautogui.moveTo(wScr - clocX, clocY)
    return clocX, clocY

def clear(temp):
    if not temp:
        return True

category_id_for_mouse_action = {
    1: CursorMovement,
    2: MouseLeftClick,
    3: MouseRightClick,
    4: ScreenShot,
    5: clear,
}
