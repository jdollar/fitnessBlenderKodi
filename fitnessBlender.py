import sys

from resources.lib.fitnessblender.constants import Constants

import requests
from bs4 import BeautifulSoup 

import re
import urlparse
import urllib
import xbmcgui
import xbmc
import xbmcplugin


basePluginUrl = sys.argv[0][:-1]
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')
fitnessBlenderBaseUrl = 'https://www.fitnessblender.com'
dialog = xbmcgui.Dialog()

args = urlparse.parse_qs(sys.argv[2][1:])
typeParam = args.get(Constants.TYPE_PARAM, None)
link = args.get(Constants.LINK_PARAM, None)
keywordParam = args.get(Constants.KEYWORD_PARAM, None)
videoPageNum = args.get(Constants.PAGE_NUM_PARAM, '1')

def buildMainMenu():
    for menuItemKey, menuItemValue in Constants.mainMenuItems.items():
        url = buildUrl({Constants.TYPE_PARAM:menuItemValue})
        li = xbmcgui.ListItem(menuItemKey, iconImage=Constants.DEFAULT_VIDEO_IMAGE)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

def buildUrl(params):
    return basePluginUrl + '?' + urllib.urlencode(params)

def findAllVideoLinksOnPage(params):
    response = requests.request('GET', fitnessBlenderBaseUrl + '/videos?' + urllib.urlencode(params))
    print(response.text)
    soup = BeautifulSoup(response.text,'html.parser')
    return soup

def generateVideoLinks(videoLinkList, paramList=None):
    for videoLink in videoLinkList:
        image = videoLink.find('img')
        updatedParams = paramList.copy() if paramList is not None else {}
        updatedParams.update({Constants.LINK_PARAM:videoLink['href'][8:]})
        url = buildUrl(updatedParams)
        li = xbmcgui.ListItem(image['alt'], iconImage=fitnessBlenderBaseUrl + image['src'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
   
    generateNextPageItem(paramList)
    xbmcplugin.endOfDirectory(addon_handle)

def generateNextPageItem(paramList):
    updatedParams = paramList.copy() if paramList is not None else {}
    updatedParams.update({Constants.PAGE_NUM_PARAM:str(int(videoPageNum[0])+1), Constants.TYPE_PARAM:typeParam[0]})
    url = buildUrl(updatedParams)
    li = xbmcgui.ListItem('Next Page', iconImage=Constants.DEFAULT_VIDEO_IMAGE)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

def getVideoId():
    response = requests.request('GET', fitnessBlenderBaseUrl + '/videos/' + link[0])
    soup = BeautifulSoup(response.text, 'html.parser')
    iframeFound = soup.find('iframe',src=re.compile('youtube'))
    return re.search('embed/(?P<video_id>.+)\?', iframeFound['src']).group('video_id')

def playVideo(videoId):
    xbmc.executebuiltin('XBMC.PlayMedia(plugin://plugin.video.youtube/play/?video_id=' + videoId + ')')

if typeParam is None:
    buildMainMenu()
elif typeParam[0] == Constants.ALL_VIDEO_MENU_ITEM:
    soup = findAllVideoLinksOnPage({'p':videoPageNum[0]})
    videoLinkList = soup.find_all('a',class_='videolink')
    generateVideoLinks(videoLinkList)
elif typeParam[0] == Constants.SEARCH_VIDEO_MENU_ITEM:
    keywordInput = dialog.input('Keyword', type=xbmcgui.INPUT_ALPHANUM) if keywordParam is None else keywordParam[0]
    soup = findAllVideoLinksOnPage({'p':videoPageNum[0],'keyword':keywordInput})
    videoLinkList = soup.find_all('a',class_='videolink')
    generateVideoLinks(videoLinkList, {'keyword':keywordInput})
else:
    playVideo(getVideoId())


