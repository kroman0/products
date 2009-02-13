from Products.CMFCore.utils import getToolByName
from quills.app.portlets.weblogadmin import *

class CustomRenderer(Renderer):

    _template = ViewPageTemplateFile('weblogadmin.pt')


    @property
    def weblog_url(self):
        weblog_content = self.getWeblogContentObject()
        return weblog_content.absolute_url()

    @property
    def create_url(self):
        weblog_content = self.getWeblogContentObject()
        try:
            config = IWeblogEnhancedConfiguration(weblog_content)
            type_name = config.default_type
        except TypeError: # Could not adapt, so fall back to default.
            type_name = 'WeblogEntry'
        return "/createObject?type_name=%s" % type_name

    @property
    def options(self):
        weblog_content = self.getWeblogContentObject()
        catalog = getToolByName(self.context, 'portal_catalog')
        bfolders = catalog(
            path='/'.join(weblog_content.getPhysicalPath()),
            portal_type='Folder'
        )
        wc_path_len = len('/'.join(weblog_content.getPhysicalPath()))
        cats = [b.getPath()[wc_path_len+1:] for b in bfolders if not len(b.getPath())==wc_path_len ]
        return cats
                
