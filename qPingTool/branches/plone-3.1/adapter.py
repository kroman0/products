from zope.component import adapts
from zope.interface import Interface, implements

from interfaces import IPingTool
from Products.CMFCore.utils import getToolByName

class ICanonicalURL(Interface):
    """ Interface for canonical URL API providing."""

    def getCanonicalURL():
        """Get canonical_url property value."""

    #def setCanonicalURL():
        #"""Set canonical_url property value."""

    #def addCanonicalURL(value):
        #"""Add canonical_url property value"""

    #def hasCanonicalURL():
        #"""Check if portal has canonical_url property"""


class CanonicalURL(object):
    """ CanonicalURL adapter
    """
    adapts(IPingTool)
    implements(ICanonicalURL)

    def __init__(self, context):
        """ init
        """
        self.context = context

    def getCanonicalURL(self):
        """Get canonical_url property value
        """
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        return portal.getProperty('canonical_url',None)

    #def setCanonicalURL(self, value):
        #"""Update canonical_url property value
        #"""
        #portal = getToolByName(self, 'portal_url').getPortalObject()
        #portal.manage_changeProperties(canonical_url=str(value))


    #def addCanonicalURL(self, value):
        #"""Add canonical_url property value
        #"""
        #portal = getToolByName(self, 'portal_url').getPortalObject()
        #if not portal.hasProperty('canonical_url'):
            #portal.manage_delProperties(ids=['canonical_url'])
        #portal.manage_addProperty('canonical_url', str(value), 'string')


    #def hasCanonicalURL(self):
        #"""Check if portal has canonical_url property
        #"""
        #portal = getToolByName(self, 'portal_url').getPortalObject()
        #return portal.hasProperty('canonical_url')
