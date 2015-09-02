import xbmcgui

class FilterGUI(xbmcgui.WindowXMLDialog):
   def __init__(self, *args, **kwargs):
       xbmcgui.WindowXMLDialog.__init__(self, *args, **kwargs) 
