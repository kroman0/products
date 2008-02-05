from zope.app.event import objectevent
from p4a.audio.atct import _atct
from p4a.audiopatch.interfaces import IAudioEncoded

class AudioEncodingChangedEvent(objectevent.ObjectEvent):
    """Audio encoding changed.
    """ 
    
#event handler for IObjectModifiedEvent,
#which repeats all functionality of _atct.sync_audio_metadata
#but adds some neccesary assignment
def sync_audio_metadata(obj, evt):
    __doc__ = _atct.sync_audio_metadata.__doc__
    
    _atct.sync_audio_metadata(obj, evt)
    
    #audio._save_audio_metadata() stores id3 tag in 2.4 version
    #and converts tag's text frames to 'utf-8'. That's why original_encoding
    #will be different, also encoding isn't useful now. 
    #And we must set encoding and original_encoding to "".
    #
    #raised AttributeError: can't set attribute, but I don't know why
    #
    audio_encoded = IAudioEncoded(obj)
    audio_encoded.original_encoding = ""
    audio_encoded.encoding = ""
    
    #from zope.app.annotation.interfaces import IAnnotations
    #from p4a.audiopatch.adapters import _ATCTFileAudioEncoded
    #
    #encoding_data = IAnnotations(obj).get(_ATCTFileAudioEncoded.ENCODING_KEY)
    #encoding_data["encoding"] = encoding_data["original_encoding"] = ""