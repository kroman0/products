from zope.component.interface import interfaceToName
from Products.CMFCore.utils import getToolByName
from quills.app.browser.baseview import BaseView
from quills.core.interfaces.enabled import IPossibleWeblog

class WebLogCatSearch(BaseView):
    """
        Actually this view is migrated SimpleBlogCatSearch
        template. 
    """

    def __call__(self):
        """
            Returns entries list by specified category.
        """

        context = self.context.aq_inner
        category = self.request.get('category', None)
        portal = getToolByName(context, 'portal_url').getPortalObject()

        if category:
            #XXX'dui-library folder should not be hardcoded here, it should be
            #searched as main weblog folder (archive)
            url = "%s/dui-library/topics/%s"%(portal.absolute_url(), category)
            return self.request.response.redirect(url)
