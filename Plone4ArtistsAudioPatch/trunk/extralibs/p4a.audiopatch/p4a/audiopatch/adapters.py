from zope import interface
from zope import component

from p4a.audio.interfaces import IAudio, IAudioEnhanced
from Products.ATContentTypes.interface import IATFile
from p4a.audio.atct._atct import _ATCTFileAudio
from p4a.audiopatch.interfaces import IAudioEncoded

from zope.app.annotation.interfaces import IAnnotations
from persistent.dict import PersistentDict

from zope.event import notify
from p4a.audiopatch.events import AudioEncodingChangedEvent

from p4a.fileimage import utils
from p4a.audio.mp3.thirdparty import eyeD3
import os


#need to override existing adapter form IATFile to IAudio
@interface.implementer(IAudio)
@component.adapter(IATFile)
def ATCTFileAudioOverriding(context):
    if not IAudioEnhanced.providedBy(context):
        return None
    return _ATCTFileAudioEncoded(context)


@interface.implementer(IAudioEncoded)
@component.adapter(IATFile)
def ATCTFileAudioEncoded(context):
    if not IAudioEnhanced.providedBy(context):
        return None
    return _ATCTFileAudioEncoded(context)

class _ATCTFileAudioEncoded(_ATCTFileAudio):
    """An IAudioEncoded adapter that handle ATCT based file content.
    """
    interface.implements(IAudioEncoded)

    ENCODING_KEY = "p4a.patch.adapters.ATCTFileAudioEncoded"

    def __init__(self, context):
        _ATCTFileAudio.__init__(self, context)
        annotations = IAnnotations(context)
        self.encoding_data = annotations.get(self.ENCODING_KEY, None)
        if self.encoding_data == None:
            self.encoding_data = PersistentDict()
            annotations[self.ENCODING_KEY] = self.encoding_data
            self.encoding_data['encoding'] = ""
            self.encoding_data['original_encoding'] = ""

    def getEncoding(self):
        """get encoding"""
        return self.encoding_data['encoding']
        
    def setEncoding(self, value):
        """set encoding"""
        self.encoding_data['encoding'] = value
        notify(AudioEncodingChangedEvent(self.context))
 
    encoding = property(getEncoding, setEncoding)
    
    def get_original_encoding(self):
        if not self.encoding_data['original_encoding'] and self.audio_type == "MP3":
            filename = utils.write_ofsfile_to_tempfile(self.context.getRawFile())
            tag = eyeD3.Tag()
            tag.link(filename)
            for f in tag.frames:
                if self.encoding_data['original_encoding']: break
                if isinstance(f, eyeD3.frames.TextFrame):
                    self.encoding_data['original_encoding'] = eyeD3.id3EncodingToString(f.encoding)
            os.remove(filename)
        return self.encoding_data['original_encoding']
	
    def set_original_encoding(self, value):
	self.encoding_data['original_encoding'] = value
	
    original_encoding = property(get_original_encoding, set_original_encoding)

    @property
    def title(self):
        data = self.audio_data.get('title', None)
        if self.audio_type == "MP3" and self.encoding and self.original_encoding and isinstance(data, unicode):
            data = data.encode(self.original_encoding, 'replace').decode(self.encoding, 'replace')
        return data 

    @property
    def artist(self):
        data = self.audio_data.get('artist', None)    
        if self.audio_type == "MP3" and self.encoding and self.original_encoding and isinstance(data, unicode):
            data = data.encode(self.original_encoding, 'replace').decode(self.encoding, 'replace')
        return data
        
    @property
    def album(self):
        data = self.audio_data.get('album', None)    
        if self.audio_type == "MP3" and self.encoding and self.original_encoding and isinstance(data, unicode):
            data = data.encode(self.original_encoding, 'replace').decode(self.encoding, 'replace')
        return data
        
    @property
    def comment(self):
        data = self.audio_data.get('comment', None)    
        if self.audio_type == "MP3" and self.encoding and self.original_encoding and isinstance(data, unicode):
            data = data.encode(self.original_encoding, 'replace').decode(self.encoding, 'replace')
        return data
        
    def __str__(self):
        return '<p4a.audiopatch.adapters.ATCTFileAudioEncoded title=%s>' % self.title
    __repr__ = __str__