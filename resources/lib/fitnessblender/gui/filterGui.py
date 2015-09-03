import xbmcgui

class FilterGUI(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self, *args, **kwargs)

    def close(self):
        xbmcgui.Dialog().ok('test', 'inClose')
        xbmcgui.WindowXMLDialog.close(self)

    def getSearchParameters(self):
        xbmcgui.Dialog().ok('test', str(self.getControl(1101).isSelected()))
