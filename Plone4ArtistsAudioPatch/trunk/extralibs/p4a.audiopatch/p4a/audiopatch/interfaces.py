from zope.interface import Interface, Attribute

class IAudioEncoded(Interface):
    """Interface that works with audio tag's text encoding stored in annotation"""
    
    encoding = Attribute("real (defined by user) audio tag encoding")
    
    original_encoding = Attribute("getted by eyeD3 module audio tag encoding") 
        
class IAudioEncodedView(Interface):
    """view for encoding action
    """
    def title(): 
        """return audio title"""

    def artist():
        """return audio artist"""  
  
    def album():
        """return audio album"""

    def comment():
        """return audio comment"""

    def encoding():
        """audio tag's text encoding"""

    def setEncoding(value):
        """set audio tag encoding"""

    def getEncodingsList():
        """get list of possible python text encodings"""
