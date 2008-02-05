from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFPlone.PloneFolder import PloneFolder
from config import TOOL_ID, PROJECTNAME
from Products.Archetypes.public import *
from Acquisition import aq_base
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.CMFCore.utils import UniqueObject
from Globals import InitializeClass
from errors import BlacklistedURL
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from zLOG import LOG
import re, os
from config import *

def _parseLine(line):
    parts = line.split('#')
    pattern = parts[0].strip()
    return re.compile(pattern)

def stripUrl(url):
    """cut all prefixes from url"""
    if url.startswith('http://'):
        url = url[7:]
    if url.startswith('www.'):
        url = url[4:]
    if url.endswith('/'):
        url = url[:-1]
    return url
   
class TrackSpamTool(UniqueObject, SimpleItem, PropertyManager, ActionProviderBase):
    """ This tool has to validate for spam
    """

    security = ClassSecurityInfo()

    id = TOOL_ID
    meta_type= TOOL_METATYPE
    title = 'TrackSpam Tool'
    plone_tool = True

    __implements__ = (SimpleItem.__implements__, 
                      ActionProviderBase.__implements__)

    blacklist = []
    blacklist_compiled = []

    def loadInitialFile(self):
        if not self.blackList:
            txtpath = os.path.join( os.path.dirname(__file__), 'mt_blacklist.txt' )
            fp = file(txtpath, 'r')
            for line in fp:
                line = line.strip()
                if line and not line.startswith('#'):
                    self.blacklist_compiled.append( _parseLine(line) )
            del fp

    def checkTrackback(self, trackback):
        url = trackback.getURL()
        for regexp in self.blacklist_compiled:
            match = regexp.search(url)
            if match:
                return 0 #raise BlacklistedURL(url, match)
        return 1

    def checkURL(self, url):
        if not url:
            return 0
        for regexp in self.blacklist_compiled:
            match = regexp.search(url)
            if match:
                return 0 #raise BlacklistedURL(url, match)
        return 1

    def getBlackList(self):
        """ return list for editing """
        return '\n'.join(self.blacklist)

    def setBlackList(self, data):
        """ save the blacklist """
        lines = [l.strip() for l in data.split('\n')]
        res=[]
        for r in lines:
            if lines.index(r)+1<len(lines)-1:
                linesc = lines[lines.index(r)+1:]
                if r not in linesc:
                    res.append(r)
            else:
                res.append(r)
        self.blacklist = res
        self.blacklist_compiled = [_parseLine(r) for r in res]

    def blackListAndRemove(self, trbacks_checked):
        """ add the entries to black list remove them and the similar ones """
        if not trbacks_checked:
            return 0, 0
        uid_catalog = getToolByName(self, 'uid_catalog')
        catalog = getToolByName(self, 'portal_catalog')
        urls = []
        counter = 0
        bl_counter = 0
        for trb in trbacks_checked:
            obj = uid_catalog(UID=trb)[0].getObject()
            geturl = obj.getUrl()
            urls.append(geturl)
            url = stripUrl(geturl)
            if url not in self.blacklist:
                self.blacklist.append(url)
                self.blacklist_compiled.append(_parseLine(url))
                bl_counter += 1
            obj.aq_parent.manage_delObjects([obj.getId()])
            counter += 1
        res = catalog(portal_type='TrackBack', review_state='pending',sort_on='Date')
        for r in res:
            obj = r.getObject()
            if obj.getUrl() in urls:
                obj.aq_parent.manage_delObjects([obj.getId()])
                counter += 1
        return bl_counter, counter
                

InitializeClass(TrackSpamTool)
