import requests
import urllib
import re

from bs4 import BeautifulSoup

from resources.lib.fitnessblender.constants import FITNESSBLENDER_BASE_URL 

class ScrapeUtil:
    def findAllVideoLinksOnPage(self, params):
        response = requests.request('GET', FITNESSBLENDER_BASE_URL + '/videos?' + urllib.urlencode(params))
        soup = BeautifulSoup(response.text,'html.parser')
        return soup

    def getVideoId(self, link):
        response = requests.request('GET', FITNESSBLENDER_BASE_URL + '/videos/' + link[0])
        soup = BeautifulSoup(response.text, 'html.parser')
        iframeFound = soup.find('iframe',src=re.compile('youtube'))
        return re.search('embed/(?P<video_id>.+)\?', iframeFound['src']).group('video_id')
