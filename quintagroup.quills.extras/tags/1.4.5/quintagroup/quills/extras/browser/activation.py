#zope imports 
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from Products.Five import BrowserView

#plone imports
from Products.statusmessages.interfaces import IStatusMessage

#quills imports
from quills.core.interfaces.enabled import IPossibleWeblog

#other imports
from quintagroup.quills.extras.browser.interfaces import IWeblogCategory

class CategoryActivation(BrowserView):
    """ This view determines if it's possible to
        activate blog category or deactivate it.
    """

    def can_activate(self):
        return IPossibleWeblog.providedBy(self.context) and \
               not IWeblogCategory.providedBy(self.context)

    def can_deactivate(self):
        return IWeblogCategory.providedBy(self.context)

class ActivateBlogCategory(BrowserView):

    def __call__(self):
        if IWeblogCategory.providedBy(self.context):
            # deactivate blog category
            noLongerProvides(self.context, IWeblogCategory)
            #return to default folder view
            self.context.setLayout('folder_listing')
            msg = 'blog categroy deactivated'
        elif IPossibleWeblog.providedBy(self.context):
            alsoProvides(self.context, IWeblogCategory)
            #set appropriate view for weblog category
            self.context.setLayout('weblogfolder_view')
            msg = 'blog category activated'
        else:
            msg = 'not bloggable'

        IStatusMessage(self.request).addStatusMessage(msg, type='info')
        self.request.response.redirect(self.context.absolute_url())
