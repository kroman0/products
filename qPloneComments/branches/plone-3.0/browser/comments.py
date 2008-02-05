from Acquisition import aq_inner
from AccessControl import getSecurityManager
from Products.CMFPlone.utils import getToolByName

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import comments

class CommentsViewlet(comments.CommentsViewlet):
    """A custom version of the comments viewlet 
    """

    render = ViewPageTemplateFile('comments.pt')
    
    def is_moderation_enabled(self):
        """ Returns a boolean indicating whether the user has enabled moderation
            in the qPloneComments configlet
        """
        portal_properties = getToolByName(self.context, 'portal_properties')
        try:
            return portal_properties.qPloneComments.getProperty('enable_moderation', None)
        except AttributeError:
            return False
        
    def can_moderate(self):
        """ Returns a boolean indicating whether the user has the 'Moderate Discussion'
            permission
        """
        return getSecurityManager().checkPermission('Moderate Discussion', aq_inner(self.context))
