from Products.CMFDefault.DiscussionItem import DiscussionItemContainer, DiscussionItem
from AccessControl import getSecurityManager, Unauthorized
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from utils import *

# Patching createReply method of 
# Products.CMFDefault.DiscussionItem.DiscussionItemContainer
def createReply( self, title, text, Creator=None, email=''):
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
        if hasattr(item, 'addCreator'):
            item.addCreator(Creator)
        else:
            item.creator = Creator

    pm = getToolByName(self, 'portal_membership')

    if pm.isAnonymousUser():
        userid = 'anonym'
    else:
        userid = pm.getAuthenticatedMember().getId()

    item.manage_addProperty(id='userid', value=userid, type='string')
    item.manage_addProperty(id='email', value=email, type='string')

    item.review_state="private"

    item.setReplyTo( self._getDiscussable() )
    self._container[ id ] = item

    # Control of performing moderation
    ifModerate = getProp(self, "enable_moderation", marker=False)
    if ifModerate:
        roles = [role['name'] for role in self.acl_users.rolesOfPermission('Moderate Discussion')
                 if role['selected']== 'SELECTED']
        roles.append('DiscussionManager')
        item.manage_permission('Delete objects', roles, acquire=1)
        item.manage_permission('View', roles, acquire=0)
    else:
        item.review_state = "published"

    item.__of__( self ).indexObject()
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

perms = DiscussionItemContainer.__ac_permissions__
new_perms = []
for item in perms:
    perm_name = item[0]
    funcs = item[1]
    if 'deleteReply' in funcs:
        new_perms.append( (perm_name, [f for f in funcs if f != 'deleteReply']) )
        new_perms.append( ('Moderate Discussion', ('deleteReply', )) )
    else:
        new_perms.append(item)

DiscussionItemContainer.__ac_permissions__ = new_perms
InitializeClass(DiscussionItemContainer)

DiscussionItemContainer.createReply = createReply
DiscussionItemContainer.getReplies = getReplies