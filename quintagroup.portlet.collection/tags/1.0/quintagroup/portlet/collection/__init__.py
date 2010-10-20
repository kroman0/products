from zope.i18nmessageid import MessageFactory
MessageFactory = MessageFactory('quintagroup.portlet.collection')

from Products.CMFCore.permissions import setDefaultRoles

PROJECTNAME = "quintagroup.portlet.collection"
DEFAULT_ADD_CONTENT_PERMISSION = "%s: Add collection portlet" % PROJECTNAME

setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner',))
