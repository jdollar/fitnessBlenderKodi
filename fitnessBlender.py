import sys

import requests
from bs4 import BeautifulSoup 

import xbmcgui
import xbmcplugin

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')
fitnessBlenderBaseUrl = 'https://www.fitnessblender.com'

def findAllVideoLinks():
    response = requests.request('GET', fitnessBlenderBaseUrl + '/videos');
    soup = BeautifulSoup(response.text,'html.parser')
    return soup

def generateVideoLinks(videoLinkList):
    for videoLink in videoLinkList:
        image = videoLink.find('img')
        li = xbmcgui.ListItem(image['alt'], iconImage=fitnessBlenderBaseUrl + image['src'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=videoLink['href'], listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)


soup = findAllVideoLinks()
videoLinkList = soup.find_all('a',class_='videolink')
generateVideoLinks(videoLinkList)
