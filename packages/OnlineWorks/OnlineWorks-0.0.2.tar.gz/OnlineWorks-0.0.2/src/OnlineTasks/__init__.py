"""
Python module for sevaral online tasks like:

: Playing video on youtube
: Get Space Nasa News
: To Get Covid 19 Cases, Deaths, Recovered
: To get the title of a website
: To search on google
: To get your public ip address
: To open your mobile camera on your computer
"""

import requests
from bs4 import BeautifulSoup
import webbrowser as web
import os
import cv2
import numpy as np
import urllib.request

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

try:
    import pafy
except:
    print("Installing youtube-dl module beacuse the pafy can not be started without youtube-dl")
    os.system('pip install youtube-dl')

__version__ = '0.0.2'
__author__ = "Debadrito Dutta (dipalidutta312@gmail.com)"
__copyright__ = "Copyright (c) 2021-2022 Debadrito Dutta"
__license__ = 'Public Domain'

modules_used = [
    'requests',
    'bs4',
    'webbrowser',
    'pafy',
    'opencv-python',
    'numpy',
    'urlib.request',
]

class Youtube:
    def __init__(self):
        self.working = True
    def load(self, topic):
        """
        Loads a video according to the topic speccified
        It will pick up the first video and load it
        Also, it will return information about the video
        """
        if 'requests' not in modules_used:
            raise ModuleNotLoaded("You cant use this function beacuse the requests module can not be loaded!")
        elif 'pafy' not in modules_used:
            raise ModuleNotLoaded("You cant use this function beacuse the pafy module can not be loaded")
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
                raise NoYoutubeVideoFound("No video found.")
            else:
                self.url = "https://www.youtube.com"+lst[count-5]
                vid = pafy.new(self.url)
                title = vid.title
                author = vid.author
                thumb = vid.thumb
                likes = vid.likes
                dislikes = vid.dislikes
                category = vid.category
                duration = vid.duration
                published = vid.published
                length_in_seconds = vid.length
                keywords = vid.keywords
                rating = vid.rating
                views = vid.viewcount
                return {'title': title, 'author': author, 'thumb': thumb, 'likes': likes, 'dislikes': dislikes, 'category': category, 'duration': duration, 'published': published, 'length': length_in_seconds, 'keywords': keywords, 'rating': rating, 'views': views}

    def play(self, browser_name='deafult-browser', browser_path='deafalt-browser-path'):
        if browser_name == 'deafult-browser' and browser_path == 'deafalt-browser-path':
            web.open_new_tab(self.url)
        else:
            webbrowser_path = r"{}".format(browser_path)
            web.register(browser_name, None, web.BackgroundBrowser(webbrowser_path))
            web.get(browser_name).open_new_tab(self.url)
            return self.url
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
    Fetches the title of a website
    """
    r = requests.get(url)
    code = r.text
    soup = BeautifulSoup(code, "html.parser")
    title = soup.find('title')
    return title.string
def search(topic, browser_name='deafult-browser', browser_path='deafult-browser-path'):
    """
    This funtion searches on google according to the topic
    """
    url = "https://google.com/search?q={}".format(topic)
    if browser_name == "deafult-browser" and browser_path == "deafult-browser-path":
        web.open_new_tab(url)
    else:
        path = r"{}".format(browser_path)
        web.register(browser_name, None, web.BackgroundBrowser(path))
        web.get(browser_name).open_new_tab(url)