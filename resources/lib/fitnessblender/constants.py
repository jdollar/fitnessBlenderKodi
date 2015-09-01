import sys

BASE_APP_URL = sys.argv[0][:-1]
FITNESSBLENDER_BASE_URL = 'https://www.fitnessblender.com'

ADDON_HANDLE = int(sys.argv[1])

ALL_VIDEO_MENU_ITEM = 'allVideos'
SEARCH_VIDEO_MENU_ITEM = 'searchVideos'
VIDEO_MENU_ITEM = 'video'

TYPE_PARAM = 'type'
LINK_PARAM = 'link'
KEYWORD_PARAM = 'keyword'
PAGE_NUM_PARAM = 'pageNum'

DEFAULT_VIDEO_IMAGE = 'DefaultVideo.jpg'
FITNESS_BLENDER_BASE_URL = 'https://www.fitnessblender.com'

NEXT_PAGE_TEXT = 'Next Page'

MAIN_MENU_ITEMS = {
                    'Search':SEARCH_VIDEO_MENU_ITEM,
                    'All Videos':ALL_VIDEO_MENU_ITEM
                }
