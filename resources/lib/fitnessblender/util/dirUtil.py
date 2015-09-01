import sys
import xbmcgui
import xbmcplugin

from resources.lib.fitnessblender.constants import ADDON_HANDLE, \
                                                   TYPE_PARAM, \
                                                   LINK_PARAM, \
                                                   PAGE_NUM_PARAM, \
                                                   MAIN_MENU_ITEMS, \
                                                   VIDEO_MENU_ITEM, \
                                                   NEXT_PAGE_TEXT, \
                                                   DEFAULT_VIDEO_IMAGE, \
                                                   FITNESS_BLENDER_BASE_URL

from resources.lib.fitnessblender.util.urlUtil import UrlUtil

class DirUtil:
    urlUtil = UrlUtil()

    def generateVideoLinks(self, videoLinkList, paramList=None, typeParam=None):
        for videoLink in videoLinkList:
            image = videoLink.find('img')
            updatedParams = paramList.copy() if paramList is not None else {}
            updatedParams.update({TYPE_PARAM:VIDEO_MENU_ITEM, LINK_PARAM:videoLink['href'][8:]})
            url = self.urlUtil.buildUrl(updatedParams)
            li = xbmcgui.ListItem(image['alt'], iconImage=FITNESS_BLENDER_BASE_URL + image['src'])
            xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li)
        #End For 

        self.generateNextPageItem(paramList, typeParam)
        xbmcplugin.endOfDirectory(ADDON_HANDLE)
    #End generateVideoLinks

    def generateNextPageItem(self, paramList, typeParam):
        updatedParams = paramList.copy() if paramList is not None else {}
        if typeParam is not None:
            updatedParams.update({TYPE_PARAM:typeParam[0]})

        url = self.urlUtil.buildUrl(updatedParams)
        li = xbmcgui.ListItem(NEXT_PAGE_TEXT, iconImage=DEFAULT_VIDEO_IMAGE)
        xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=True)
    #End generateNextPageItem

    def buildMainMenu(self):
        for menuItemKey, menuItemValue in MAIN_MENU_ITEMS.items():
            url = self.urlUtil.buildUrl({TYPE_PARAM:menuItemValue})
            li = xbmcgui.ListItem(menuItemKey, iconImage=DEFAULT_VIDEO_IMAGE)
            xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=True)

        xbmcplugin.endOfDirectory(ADDON_HANDLE)
    #End buildMainMenu
#End DirUtil
