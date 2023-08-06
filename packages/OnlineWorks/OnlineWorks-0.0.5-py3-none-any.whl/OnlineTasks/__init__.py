"""
OnlineWorks, A library for performing online tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python module for sevaral online tasks like:

: Playing video on youtube
: Get Space Nasa News
: To Get Covid 19 Cases, Deaths, Recovered
: To get the title of a website
: To search on google
: To get your public ip address
: To open your mobile camera on your computer
: To get your location
: To send emails
: To send whatsapp message
: To send a whatsapp message to group
"""

import requests
from bs4 import BeautifulSoup
import webbrowser as web
import os
import cv2
import numpy as np
import urllib.request
import wikipedia
import smtplib
from email.mime.multipart import MIMEMultipart

# Exceptions

class NoYoutubeVideoFound(Exception):
    """
    This exception will be raised when the youtube video will not be found
    """


class NoDataAvaliableOnNasa(Exception):
    """
    This error will be raised if there is no data avaliable on nasa
    """


class ModuleNotLoaded(Exception):
    """
    This error will be raised if any module can not be loaded
    """
class YoutubeVideoNotLoaded(Exception):
    """
    This exception will be raised if you are playing a youtube video without loading it!
    """
class CantSendEmail(Exception):
    """
    This exception will be raised if the email can not be sent!
    """

__version__ = '0.0.5'
__author__ = "Debadrito Dutta (dipalidutta312@gmail.com)"
__copyright__ = "Copyright (c) 2021-2022 Debadrito Dutta"
__license__ = 'Public Domain'

modules_used = [
    'requests',
    'bs4',
    'webbrowser',
    'opencv-python',
    'numpy',
    'urlib',
    'wikipedia',
    'smtplib',
    'email',
]
sleeptm = "None, You can use this function to print the remaining time in seconds."

class Youtube:
    def __init__(self):
        self.working = True
    def load(self, topic):
        """
        Loads a video according to the topic specified
        It will pick up the first video and load it
        Also, it returns the video url that has been loaded!
        """
        if 'requests' not in modules_used:
            raise ModuleNotLoaded("You cant use this function beacuse the requests module can not be loaded!")
        else:
            url = 'https://www.youtube.com/results?q=' + topic
            count = 0
            cont = requests.get(url)
            data = cont.content
            data = str(data)
            lst = data.split('"')
            for i in lst:
                count += 1
                if i == 'WEB_PAGE_TYPE_WATCH':
                    break
            if lst[count-5] == "/results":
                # No video found.
                raise NoYoutubeVideoFound("No video found.")
            else:
                # Load the video
                self.url = "https://www.youtube.com"+lst[count-5]
                return self.url

    def play(self, browser_name='deafult-browser', browser_path='deafalt-browser-path'):
        """
        Plays the video that you have just loaded!
        """
        try:
            if browser_name == 'deafult-browser' and browser_path == 'deafalt-browser-path':
                web.open_new_tab(self.url)
            else:
                webbrowser_path = r"{}".format(browser_path)
                web.register(browser_name, None, web.BackgroundBrowser(webbrowser_path))
                web.get(browser_name).open_new_tab(self.url)
        except:
            raise YoutubeVideoNotLoaded("You did'nt loaded a video! Please load a video first!")
def get_corona_info(Country):
    """
    Returns corona deaths, cases and recovered in a dict format
    Also, install the lxml module for using this function
    To install the lxml module
    Just Type:
    pip install lxml
    """
    if 'requests' not in modules_used:
        raise ModuleNotLoaded("You cant use this function beacuse the requests module can not be loaded")
    elif 'bs4' not in modules_used:
        raise ModuleNotLoaded("You cant use this function beacuse the bs4 module can not be loaded")
    else:
        countries = str(Country)
        url = "https://www.worldometers.info/coronavirus/country/{}".format(countries)
        result = requests.get(url)
        soups = BeautifulSoup(result.text, 'lxml')
        corona = soups.find_all('div', class_='maincounter-number')
        Data = []
        for case in corona:
            span = case.find('span')
            Data.append(span.string)
        cases, Death, recovered = Data
        dicatnary_of_data = {'cases': cases, 'deaths': Death, 'recovered': recovered}
        return dicatnary_of_data
def get_ip_address():
    """
    Returns the public ip address
    """
    ip = requests.get('https://api.ipify.org').text
    return ip
def open_mobile_camera(ipwebcam_ip):
    """
    Step 1: Download and install the ip webcam app from the play store from your mobile
    Step 2: Open the ip webcam app, and then click on start server
    Step 3: Now, you will get an IPV4, so, write that on the argument 'ipwebcam_ip'
    Step 4: Call this function and then run
    Step 5: Then run and you will se your mobile camera on your computer!
    """
    URL = "http://{}/shot.jpg".format(ipwebcam_ip)
    while True:
        img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        cv2.imshow('Mobile Camera', img)
        q = cv2.waitKey(1)
        if q == ord("q"):
            break
        cv2.destroyAllWindows()
def fetch_title(url):
    """
    Fetches the title of a website and returns in a string form.
    """
    r = requests.get(url)
    code = r.text
    soup = BeautifulSoup(code, "html.parser")
    title = soup.find('title')
    return title.string
def search(topic, browser_name='deafult-browser', browser_path='deafult-browser-path'):
    """
    This funtion searches on google according to the topic
    And also returns some information of the topic!
    If there is no information avalaible,
    It will just return None
    """
    url = "https://google.com/search?q={}".format(topic)
    if browser_name == "deafult-browser" and browser_path == "deafult-browser-path":
        web.open_new_tab(url)
    else:
        path = r"{}".format(browser_path)
        web.register(browser_name, None, web.BackgroundBrowser(path))
        web.get(browser_name).open_new_tab(url)
    
    try:
        result = wikipedia.summary(topic)
        return result
    except:
        return None
def get_location(api_key):
    """
    Step 1: Register in https://ipgeolocation.abstractapi.com
    Step 2: Get your api key
    Step 3: Give your api key in the parameter 'api_key'
    """
    response = "https://ipgeolocation.abstractapi.com/v1/?api_key={}".format(api_key)
    geo_requests = requests.get(response)
    geo_data = geo_requests.json()
    city = geo_data['city']
    country = geo_data['country']
    state = geo_data['region']
    Data = city, country, state
    return Data
def SendEmail(email, password, to, subject='', body=''):
    """
    This function will send email!
    To use this function,
    You have to enable the less secure apps setting!
    Otherwise, it will raise CantSendEmail Exception!
    """
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['Body'] = body
        msg['From'] = email
        msg['To'] = to
        text = msg.as_string()

        server.sendmail(email, to, text)
        server.quit()
    except Exception as e:
        raise CantSendEmail("This email can not be sent to {}".format(to))
def OpenPlaceInGoogleMaps(Place, browser_name='deafult-browser', browser_path='default-browser-path'):
    """
    Opens a place in google maps
    """
    Url_place = "https://www.google.com/maps/place/" + str(Place)
    if browser_name == 'deafult-browser' and browser_path == 'default-browser-path':
        web.open_new_tab(Url_place)
    else:
        path = r"{}".format(browser_path)
        web.register(browser_name, None, web.BackgroundBrowser(path))
        web.get(browser_name).open_new_tab(Url_place)