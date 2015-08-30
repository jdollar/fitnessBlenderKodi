import sys

import requests
from bs4 import BeautifulSoup 

import re
import urlparse
import urllib
import xbmcgui
import xbmc
import xbmcplugin

basePluginUrl = sys.argv[0]
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')
fitnessBlenderBaseUrl = 'https://www.fitnessblender.com'

args = urlparse.parse_qs(sys.argv[2][1:])
video = args.get('video', None)
link = args.get('link', None)

def buildUrl(params):
    return basePluginUrl + '?' + urllib.urlencode(params)

def findAllVideoLinks():
    response = requests.request('GET', fitnessBlenderBaseUrl + '/videos')
    soup = BeautifulSoup(response.text,'html.parser')
    return soup

def generateVideoLinks(videoLinkList):
    for videoLink in videoLinkList:
        image = videoLink.find('img')
        li = xbmcgui.ListItem(image['alt'], iconImage=fitnessBlenderBaseUrl + image['src'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=basePluginUrl + '?video=true&link=' + videoLink['href'][8:], listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)

if video is None:
	soup = findAllVideoLinks()
	videoLinkList = soup.find_all('a',class_='videolink')
	generateVideoLinks(videoLinkList)
elif video[0] == 'true':
	dialog = xbmcgui.Dialog()
	response = requests.request('GET', fitnessBlenderBaseUrl + '/videos/' + link[0])
	soup = BeautifulSoup(response.text, 'html.parser')
	iframeFound = soup.find('iframe',src=re.compile('youtube'))
	xbmc.Player().play('http:' + iframeFound['src'] + '&autoplay=1')
