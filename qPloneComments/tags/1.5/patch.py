#from Products.CMFCore.CMFCorePermissions import ReplyToItem, View
from Products.CMFDefault.DiscussionItem import DiscussionItemContainer, DiscussionItem
from AccessControl import getSecurityManager, Unauthorized
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

#from config import *
from utils import *

# Patching createReply method of 
# Products.CMFDefault.DiscussionItem.DiscussionItemContainer
def createReply( self, title, text, Creator=None ):
    """
        Create a reply in the proper place
    """
    container = self._container

    id = int(DateTime().timeTime())
    while self._container.get( str(id), None ) is not None:
        id = id + 1
    id = str( id )

    item = DiscussionItem( id, title=title, description=title )
    item._edit( text_format='structured-text', text=text )

    if Creator:
        item.creator = Creator

    pm = getToolByName(self, 'portal_membership')
    value = 0
    if pm.isAnonymousUser():
        value = 1
    if item.hasProperty('isAnon'):
        item.manage_changeProperties({'id':'isAnon','value':value})
    else:
        item.manage_addProperty(id='isAnon', value=value, type='boolean')

    item.__of__( self ).indexObject()

    item.setReplyTo( self._getDiscussable() )

    self._container[ id ] = item

    # Control of performing moderation
    ifModerate = getProp(self, "Turning_on/off_Moderation", marker=False)
    if ifModerate:
        from zLOG import LOG
        LOG('qPloneComments',777,'createReply','ifModerate=%s \t that''s why Moderation was called' % str(ifModerate) )
        roles = ['Manager', 'Owner', 'Reviewer']
        item.manage_permission('View', roles, acquire=0)

    return id


def getReplies( self ):
    """
        Return a sequence of the DiscussionResponse objects which are
        associated with this Discussable
    """
    objects = []
    a = objects.append
    validate = getSecurityManager().validate

    result_ids = self._getReplyResults()
    for id in result_ids:
        object = self._container.get( id ).__of__( self ) 
        try:
            if validate(self, self, id, object):
                a( object )
        except Unauthorized:
            pass

    return objects

DiscussionItemContainer.__dict__["createReply"] =  createReply
DiscussionItemContainer.__dict__["getReplies"] =  getReplies
