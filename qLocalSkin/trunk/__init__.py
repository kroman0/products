from Products.CMFPlone.URLTool import URLTool

from adapters.interfaces import IRequestPortalUrlAnnotator

def urltool_call(self, relative=0, *args, **kw):
    """ Get by default the absolute URL of the portal. If request is annonated then add suffix to portal_url
    """

    # print '################################ Called patched portal_url __call__: ' + self.REQUEST.URL
    url_suffix = ''
    if self.REQUEST:
        annotator = IRequestPortalUrlAnnotator(self.REQUEST, None)
        if annotator is not None:
            url_suffix = annotator.getPortalUrlSuffix()
            # print '############ Added sufix to portal_url: ' + url_suffix

    return self.getPortalObject().absolute_url(relative=relative) +  url_suffix

def urltool_getPortalPath(self):
    """ Get the portal object's URL without the server URL component.
    """

    url_suffix = ''
    if self.REQUEST:
        annotator = IRequestPortalUrlAnnotator(self.REQUEST, None)
        if annotator is not None:
            url_suffix = annotator.getPortalUrlSuffix()
            # print '############ Added sufix to portal_url: ' + url_suffix

    return '/'.join(self.getPortalObject().getPhysicalPath()) + url_suffix

URLTool.__call__ = urltool_call
URLTool.getPortalPath = urltool_getPortalPath