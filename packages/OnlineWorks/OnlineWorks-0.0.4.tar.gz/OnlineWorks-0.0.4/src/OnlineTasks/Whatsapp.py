import pyautogui as pg
import time
import webbrowser as web
from urllib.parse import quote

sleeptm = "None, You can use this function to print the remaining time in seconds."

def send_whatsapp_message(phone_no, message, time_hour, time_min, wait_time=20, print_waitTime=True, browser_name='deafult', browser_path='deafult'):
    """
    Sends a whatsapp message to a number,
    Phone Number Should be in String to Integer,
    Notice: This function will not send whatsapp message if the browser's windows is Minimized.
    """
    global sleeptm
    timehr = time_hour

    if time_hour not in range(0, 25) or time_min not in range(0, 60):
        print("Invalid time format")

    if time_hour == 0:
        time_hour = 24
    callsec = (time_hour*3600)+(time_min*60)

    curr = time.localtime()
    currhr = curr.tm_hour
    currmin = curr.tm_min
    currsec = curr.tm_sec

    if currhr == 0:
        currhr = 24

    currtotsec = (currhr*3600)+(currmin*60)+(currsec)
    lefttm = callsec-currtotsec

    if lefttm <= 0:
        lefttm = 86400+lefttm

    if lefttm < wait_time:
        return False

    date = "%s:%s:%s" % (curr.tm_mday, curr.tm_mon, curr.tm_year)
    time_write = "%s:%s" % (timehr, time_min)
    sleeptm = lefttm-wait_time
    if print_waitTime:
        pass
    time.sleep(sleeptm)
    parsedMessage = quote(message)
    if browser_name == 'deafult' and browser_path == 'deafult':
        web.open_new_tab('https://web.whatsapp.com/send?phone='+phone_no+'&text='+parsedMessage)
    else:
        b = r"{}".format(browser_path)
        web.register(browser_name, None, web.BackgroundBrowser(b))
        web.get(browser_name).open_new_tab('https://web.whatsapp.com/send?phone='+phone_no+'&text='+parsedMessage)
    time.sleep(2)
    width, height = pg.size()
    pg.click(width/2, height/2)
    time.sleep(wait_time-2)
    pg.press('enter')