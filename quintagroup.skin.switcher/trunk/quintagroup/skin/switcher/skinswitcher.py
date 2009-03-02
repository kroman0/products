from urlparse import urlsplit

from Products.CMFCore.utils import getToolByName

from config import *

def setSkin(site, event):
    ps = getToolByName(site,'portal_skins')

    if USE_FS_CONFIG:
        pref = SKIN_SWITCH_PREFIX
        switch_theme = SWITCH_THEME
    else:
        pp = getToolByName(site,'portal_properties')
        ss = getattr(pp,'skin_switcher',None)
        if not ss:
            return
        pref = ss.getProperty('theme_switch_prefix', SKIN_SWITCH_PREFIX)
        switch_theme = ss.getProperty('switch_theme', SWITCH_THEME)
        
    avail_skins = ps.getSkinSelections()
    if not (pref and switch_theme and switch_theme in avail_skins):
       return

    scheme, netloc, path, query, fragm = urlsplit(event.request.URL)
    if netloc.startswith(pref):
        site.changeSkin(switch_theme)
