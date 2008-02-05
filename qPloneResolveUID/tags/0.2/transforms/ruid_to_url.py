# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2006-08-11 
# Copyright: quintagroup.com

import re
from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.interfaces import itransform

import string
letters = string.letters
_ABSOLUTE_REL_URL=r'(?P<url>(?P<protocol>http|https|ftp|mailto|file|about[:/]+?)?[%s0-9_\@\.\,\?\!\/\:\;\-\#\~\=\&\%%\+\\]+)' % letters


class ruid_to_url:
    """Transform which replaces resolve uid into urls"""
    
    __implements__ = itransform
    
    __name__ = "ruid_to_url"
    inputs  = ('text/html',)
    output = 'text/html'
    
    def __init__(self, name=None):
        if name:
            self.__name__ = name
        self.ruid_regexp = re.compile("(?P<tag>\<(?P<tag_name>a|img)[^>]*(?P<url_attr>href|src)\s*=\s*[\'|\"]?%s[\'|\"]?[\s|\>|\/])" \
                      % _ABSOLUTE_REL_URL,re.I|re.S)

    def name(self):
        return self.__name__

    def find_ruid(self, data):
        tags_url = [{m.group('tag'):m.group('url').replace('\\','/')}\
                      for m in self.ruid_regexp.finditer(data)]
        tags_ruid =  [tu for tu in tags_url if tu.values()[0].startswith('resolveuid')]
        unique_ruid = []
        [unique_ruid.append(tu.values()[0]) for tu in tags_ruid if tu.values()[0] not in unique_ruid]
        return tags_ruid, unique_ruid

    def mapRUID_URL(self, unique_ruid, portal):
        ruid_url = {}
        rc = getToolByName(portal, 'reference_catalog')
        pu = getToolByName(portal, 'portal_url')
        for ruid in unique_ruid:
            try:
                obj = rc.lookupObject(ruid.replace('resolveuid/', ''))
                ruid_url[ruid] = pu.getRelativeUrl(obj)
            except:
                ruid_url[ruid] = ruid
        return ruid_url           
    
    def convert(self, orig, data, **kwargs):
        text = orig
        tags_ruid, unique_ruid = self.find_ruid(text)
        if unique_ruid:
            ruid_url = self.mapRUID_URL(unique_ruid, kwargs['context'])
            for tag_ruid in tags_ruid:
                tag, ruid = tag_ruid.items()[0]
                text = text.replace(tag, tag.replace(ruid, ruid_url[ruid]))
        
        data.setData(text)
        return data


def register():
    return ruid_to_url()
    