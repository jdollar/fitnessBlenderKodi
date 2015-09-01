import sys

import requests
from bs4 import BeautifulSoup 

import re
import urlparse
import urllib
import xbmcgui
import xbmc
import xbmcplugin

ALL_VIDEO_MENU_ITEM = 'allVideos'

TYPE_PARAM = 'type'
LINK_PARAM = 'link'
PAGE_NUM_PARAM = 'pageNum'

DEFAULT_VIDEO_IMAGE = 'DefaultVideo.jpg'

mainMenuItems = {'Videos':ALL_VIDEO_MENU_ITEM}

basePluginUrl = sys.argv[0][:-1]
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')
fitnessBlenderBaseUrl = 'https://www.fitnessblender.com'
dialog = xbmcgui.Dialog()

args = urlparse.parse_qs(sys.argv[2][1:])
typeParam = args.get(TYPE_PARAM, None)
link = args.get(LINK_PARAM, None)
videoPageNum = args.get(PAGE_NUM_PARAM, '1')

def buildMainMenu():
    for menuItemKey, menuItemValue in mainMenuItems.items():
	dialog.ok('key', menuItemKey)
	dialog.ok('value', menuItemValue)
        url = buildUrl({TYPE_PARAM:menuItemValue})
        li = xbmcgui.ListItem(menuItemKey, iconImage=DEFAULT_VIDEO_IMAGE)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)

def buildUrl(params):
    return basePluginUrl + '?' + urllib.urlencode(params)

def findAllVideoLinksOnPage(params):
    response = requests.request('GET', fitnessBlenderBaseUrl + '/videos?' + urllib.urlencode(params))
    soup = BeautifulSoup(response.text,'html.parser')
    return soup

def generateVideoLinks(videoLinkList):
    for videoLink in videoLinkList:
        image = videoLink.find('img')
        url = buildUrl({LINK_PARAM:videoLink['href'][8:]})
        li = xbmcgui.ListItem(image['alt'], iconImage=fitnessBlenderBaseUrl + image['src'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

    #Build next page option
    url = buildUrl({PAGE_NUM_PARAM:str(int(videoPageNum[0])+1)})
    li = xbmcgui.ListItem('Next Page', iconImage=DEFAULT_VIDEO_IMAGE)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def getVideoId():
    response = requests.request('GET', fitnessBlenderBaseUrl + '/videos/' + link[0])
    soup = BeautifulSoup(response.text, 'html.parser')
    iframeFound = soup.find('iframe',src=re.compile('youtube'))
    return re.search('embed/(?P<video_id>.+)\?', iframeFound['src']).group('video_id')

def playVideo(videoId):
    xbmc.executebuiltin('XBMC.PlayMedia(plugin://plugin.video.youtube/play/?video_id=' + videoId + ')')

if typeParam is None:
    buildMainMenu()
elif typeParam is ALL_VIDEO_MENU_ITEM:
    soup = findAllVideoLinksOnPage({'p':videoPageNum[0]})
    videoLinkList = soup.find_all('a',class_='videolink')
    generateVideoLinks(videoLinkList)
else:
    playVideo(getVideoId())
