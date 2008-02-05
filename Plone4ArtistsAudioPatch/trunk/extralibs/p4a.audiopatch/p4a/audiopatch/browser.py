from Products.Five.browser import BrowserView  
from zope.interface import implements
from p4a.audiopatch.interfaces import IAudioEncodedView, IAudioEncoded
from _encodings import encodings


class AudioEncodedView(BrowserView):

    implements(IAudioEncodedView)
    
    def __init__(self, context, request):
        self.audio_info = IAudioEncoded(context) 
    
    def title(self):
        return self.audio_info.title
    
    def artist(self): 
        return self.audio_info.artist
    
    def album(self): 
        return self.audio_info.album

    def comment(self): 
        return self.audio_info.comment 
    
    def encoding(self):
        return self.audio_info.encoding
    
    def setEncoding(self, value):
        self.audio_info.encoding = value
        
    def getEncodingsList(self):  
        return encodings
