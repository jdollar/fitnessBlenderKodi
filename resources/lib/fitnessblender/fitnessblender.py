import sys
import re
import requests
import urlparse
import urllib
import xbmcgui
import xbmc
import xbmcplugin
import xbmcaddon

from bs4 import BeautifulSoup 

from resources.lib.fitnessblender.constants import *
from resources.lib.fitnessblender.util.dirUtil import DirUtil
from resources.lib.fitnessblender.util.scrapeUtil import ScrapeUtil
from resources.lib.fitnessblender.gui.filterGui import FilterGUI

class FitnessBlender:

    def __init__(self):
        xbmcplugin.setContent(ADDON_HANDLE, 'movies')

        args = urlparse.parse_qs(sys.argv[2][1:])
        self.typeParam = args.get(TYPE_PARAM, None)
        self.link = args.get(LINK_PARAM, None)
        self.keywordParam = args.get(KEYWORD_PARAM, None)
        self.videoPageNum = args.get(PAGE_NUM_PARAM, '1')

        self.nextPageNum = str(int(self.videoPageNum[0])+1)

    def allVideoSelection(self):
        soup = ScrapeUtil().findAllVideoLinksOnPage({'p':self.videoPageNum[0]})
        videoLinkList = soup.find_all('a',class_='videolink')
        DirUtil().generateVideoLinks(videoLinkList, {PAGE_NUM_PARAM:self.nextPageNum}, self.typeParam)

    def searchVideoSelection(self):
        dialog = xbmcgui.Dialog()
        keywordInput = dialog.input('Keyword', type=xbmcgui.INPUT_ALPHANUM) if self.keywordParam is None else self.keywordParam[0]
        soup = ScrapeUtil().findAllVideoLinksOnPage({'p':self.videoPageNum[0], KEYWORD_PARAM:keywordInput})
        videoLinkList = soup.find_all('a',class_='videolink')
        DirUtil().generateVideoLinks(videoLinkList, {KEYWORD_PARAM:keywordInput, PAGE_NUM_PARAM:self.nextPageNum}, self.typeParam)

    def playVideo(self, videoId):
        xbmc.executebuiltin('XBMC.PlayMedia(plugin://plugin.video.youtube/play/?video_id=' + videoId + ')')

    def run(self):


        if self.typeParam is None:
            DirUtil().buildMainMenu()
        elif self.typeParam[0] == ALL_VIDEO_MENU_ITEM:
            self.allVideoSelection()
        elif self.typeParam[0] == SEARCH_VIDEO_MENU_ITEM:
            addon = xbmcaddon.Addon('plugin.video.fitnessBlender')
            __path__ = addon.getAddonInfo('path')
            ui = FilterGUI('custom-filter-main.xml',__path__,'default')
            ui.doModal()
            ui.getSearchParameters()
            del ui

            #self.searchVideoSelection()
        else:
            self.playVideo(ScrapeUtil().getVideoId(self.link))
