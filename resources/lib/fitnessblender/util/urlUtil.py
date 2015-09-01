import urllib

from resources.lib.fitnessblender.constants import BASE_APP_URL

class UrlUtil:

    def buildUrl(self, params):
        return BASE_APP_URL + '?' + urllib.urlencode(params)
