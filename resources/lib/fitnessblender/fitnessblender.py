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

class FitnessBlender:

    def __init__(self):
        xbmcplugin.setContent(ADDON_HANDLE, 'movies')
        self.dialog = xbmcgui.Dialog()

        self.dirUtil = DirUtil()
        self.urlUtil = UrlUtil()

        self.args = urlparse.parse_qs(sys.argv[2][1:])
        self.typeParam = self.args.get(TYPE_PARAM, None)
        self.link = self.args.get(LINK_PARAM, None)
        self.keywordParam = self.args.get(KEYWORD_PARAM, None)
        self.videoPageNum = self.args.get(PAGE_NUM_PARAM, '1')


    def findAllVideoLinksOnPage(self, params):
        response = requests.request('GET', FITNESSBLENDER_BASE_URL + '/videos?' + urllib.urlencode(params))
        soup = BeautifulSoup(response.text,'html.parser')
        return soup

    def getVideoId(self):
        response = requests.request('GET', FITNESSBLENDER_BASE_URL + '/videos/' + self.link[0])
        soup = BeautifulSoup(response.text, 'html.parser')
        iframeFound = soup.find('iframe',src=re.compile('youtube'))
        return re.search('embed/(?P<video_id>.+)\?', iframeFound['src']).group('video_id')

    def playVideo(self, videoId):
        xbmc.executebuiltin('XBMC.PlayMedia(plugin://plugin.video.youtube/play/?video_id=' + videoId + ')')

    def run(self):
        if self.typeParam is None:
            DirUtil().buildMainMenu()
        elif self.typeParam[0] == ALL_VIDEO_MENU_ITEM:
            soup = self.findAllVideoLinksOnPage({'p':self.videoPageNum[0]})
            videoLinkList = soup.find_all('a',class_='videolink')
            self.dirUtil.generateVideoLinks(videoLinkList, {PAGE_NUM_PARAM:str(int(self.videoPageNum[0])+1)}, self.typeParam)
        elif self.typeParam[0] == SEARCH_VIDEO_MENU_ITEM:
            keywordInput = self.dialog.input('Keyword', type=xbmcgui.INPUT_ALPHANUM) if self.keywordParam is None else self.keywordParam[0]
            soup = self.findAllVideoLinksOnPage({'p':videoPageNum[0], KEYWORD_PARAM:keywordInput})
            videoLinkList = soup.find_all('a',class_='videolink')
            self.dirUtil.generateVideoLinks(videoLinkList, {KEYWORD_PARAM:keywordInput, PAGE_NUM_PARAM:str(int(self.videoPageNum[0])+1)}, self.typeParam)
        else:
            self.playVideo(self.getVideoId())
