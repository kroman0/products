from Products.Plone4ArtistsAudio.p4a.z2utils import pkgloader

from Products.CMFCore.DirectoryView import registerDirectory
from Products.Plone4ArtistsAudioPatch.config import *

registerDirectory(SKINS_DIR, GLOBALS)

initbuilder = pkgloader.InitBuilder(globals=globals())
initbuilder.setup_pythonpath()

def initialize(context):    
    pkgloader.load_extrazcml(initbuilder.extralibs_configured)