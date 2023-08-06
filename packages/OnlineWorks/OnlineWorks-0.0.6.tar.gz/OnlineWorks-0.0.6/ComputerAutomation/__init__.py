import pyautogui as pg
from time import sleep


def switch_window():
    """
    This switches the window of your computer. 
    Note: This is not a OnlineTask.
    """
    pg.press("alt")
    pg.keyDown("alt")
    pg.press('tab')
    sleep(1)
    pg.keyUp("alt")