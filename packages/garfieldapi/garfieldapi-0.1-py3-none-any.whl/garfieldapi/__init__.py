from bs4 import BeautifulSoup
import requests
import os.path
import os

"""
garfieldapi

A nice Garfield comic scraper
"""

__version__ = '0.1'
__author__ = 'themysticsavages'
__credits__ = 'ermel.org'

class Error(Exception):
    pass
class API404Exception(Error):
    def __init__(self, msg):
        self.msg = msg
class OSExecption(Error):
    def __init__(self, msg):
        self.msg = msg

def getimg(date, location, filename):
    comicdate = date.split('-')
    r = requests.get('https://ermel.org/garfield.php?day={}&month={}&year={}'.format(comicdate[0], comicdate[1], comicdate[2]))
    soup = BeautifulSoup(r.text, 'html.parser')
    img = soup.findAll('img')[0]

    r = requests.get(img['src'], stream=True)
    soup = BeautifulSoup(r.text, 'html.parser')

    if os.path.isdir(location):
        os.chdir(location)
    else:
        raise(OSExecption('The location you provided is incorrect! Please use a proper one.'))

    if r.status_code == 200:
        with open('{}.png'.format(filename), 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    else:
        raise(API404Exception('That comic was not found! Try formatting the date to be DD-MM-YY!'))

def getlnk(date):
    comicdate = date.split('-')
    r = requests.get('https://ermel.org/garfield.php?day={}&month={}&year={}'.format(comicdate[0], comicdate[1], comicdate[2]))
    soup = BeautifulSoup(r.text, 'html.parser')
    img = soup.findAll('img')[0]
    return img['src']