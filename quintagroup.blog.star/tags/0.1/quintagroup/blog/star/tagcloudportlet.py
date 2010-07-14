import re

from plone.memoize import ram
from plone.app.layout.navigation.root import getNavigationRoot

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from qi.portlet.TagClouds.tagcloudportlet import _cachekey
from qi.portlet.TagClouds.tagcloudportlet import Renderer as BaseRenderer

REPATH = "\%spath=[^\&]*"

class Renderer(BaseRenderer):
    """
    """

    render = ViewPageTemplateFile('tagcloudportlet.pt')

    def __init__(self, context, request, view, manager, data):
        super(Renderer, self).__init__(context, request, view, manager, data)
        self.portal = getToolByName(context, 'portal_url')

    def removePath(self, href, sep):
        newhref = re.sub(REPATH % sep, sep, href)
        return re.sub("%s$" % sep, "", newhref)

    @ram.cache(_cachekey)
    def getTags(self):
        res = BaseRenderer.getTags(self)
        if self.root:
            navblogurl = getNavigationRoot(self.context,
                relativeRoot=self.root)
            blog = self.portal.restrictedTraverse(navblogurl)
            href_base = blog.absolute_url()
        else:
            href_base = self.portal_url

        for d in res:
            old_href = d["href"]
            q = "?" + old_href.split("?")[1]
            if '&path=' in q:
                newq = self.removePath(q, "&")
            elif '?path=' in q:
                newq = self.removePath(q, "?")
            else:
                newq = ''
            d['href'] = href_base + newq

        return res
