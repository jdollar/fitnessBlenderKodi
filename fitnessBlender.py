import sys
import re
import requests
import urlparse
import urllib
import xbmcgui
import xbmc
import xbmcplugin

from bs4 import BeautifulSoup 

from resources.lib.fitnessblender.constants import *
from resources.lib.fitnessblender.util.dirUtil import DirUtil
from resources.lib.fitnessblender.util.urlUtil import UrlUtil

xbmcplugin.setContent(ADDON_HANDLE, 'movies')
dialog = xbmcgui.Dialog()

dirUtil = DirUtil()
urlUtil = UrlUtil()

args = urlparse.parse_qs(sys.argv[2][1:])
typeParam = args.get(TYPE_PARAM, None)
link = args.get(LINK_PARAM, None)
keywordParam = args.get(KEYWORD_PARAM, None)
videoPageNum = args.get(PAGE_NUM_PARAM, '1')

def findAllVideoLinksOnPage(params):
    response = requests.request('GET', FITNESSBLENDER_BASE_URL + '/videos?' + urllib.urlencode(params))
    soup = BeautifulSoup(response.text,'html.parser')
    return soup

def getVideoId():
    response = requests.request('GET', FITNESSBLENDER_BASE_URL + '/videos/' + link[0])
    soup = BeautifulSoup(response.text, 'html.parser')
    iframeFound = soup.find('iframe',src=re.compile('youtube'))
    return re.search('embed/(?P<video_id>.+)\?', iframeFound['src']).group('video_id')

def playVideo(videoId):
    xbmc.executebuiltin('XBMC.PlayMedia(plugin://plugin.video.youtube/play/?video_id=' + videoId + ')')

if typeParam is None:
    DirUtil().buildMainMenu()
elif typeParam[0] == ALL_VIDEO_MENU_ITEM:
    soup = findAllVideoLinksOnPage({'p':videoPageNum[0]})
    videoLinkList = soup.find_all('a',class_='videolink')
    dirUtil.generateVideoLinks(videoLinkList, {PAGE_NUM_PARAM:str(int(videoPageNum[0])+1)}, typeParam)
elif typeParam[0] == SEARCH_VIDEO_MENU_ITEM:
    keywordInput = dialog.input('Keyword', type=xbmcgui.INPUT_ALPHANUM) if keywordParam is None else keywordParam[0]
    soup = findAllVideoLinksOnPage({'p':videoPageNum[0], KEYWORD_PARAM:keywordInput})
    videoLinkList = soup.find_all('a',class_='videolink')
    dirUtil.generateVideoLinks(videoLinkList, {KEYWORD_PARAM:keywordInput, PAGE_NUM_PARAM:str(int(videoPageNum[0])+1)}, typeParam)
else:
    playVideo(getVideoId())


