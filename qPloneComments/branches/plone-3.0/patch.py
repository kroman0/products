from Products.CMFDefault.DiscussionItem import DiscussionItemContainer, DiscussionItem
from AccessControl import getSecurityManager, Unauthorized
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
import rfc822
from StringIO import StringIO
from utils import *

def _mungeHeaders( messageText, mto=None, mfrom=None, subject=None):
    """Sets missing message headers, and deletes Bcc.
       returns fixed message, fixed mto and fixed mfrom"""
    mfile=StringIO(messageText.lstrip())
    mo=rfc822.Message(mfile)

    # Parameters given will *always* override headers in the messageText.
    # This is so that you can't override or add to subscribers by adding them to
    # the message text.
    if subject:
        mo['Subject'] = subject
    elif not mo.getheader('Subject'):
        mo['Subject'] = '[No Subject]'

    if mto:
        if isinstance(mto, basestring):
            mto = [rfc822.dump_address_pair(addr) for addr in rfc822.AddressList(mto) ]
        if not mo.getheader('To'):
            mo['To'] = ','.join(mto)
    else:
        mto = []
        for header in ('To', 'Cc', 'Bcc'):
            v = mo.getheader(header)
            if v:
                mto += [rfc822.dump_address_pair(addr) for addr in rfc822.AddressList(v)]
        if not mto:
            raise MailHostError, "No message recipients designated"

    if mfrom:
        mo['From'] = mfrom
    else:
        if mo.getheader('From') is None:
            raise MailHostError,"Message missing SMTP Header 'From'"
        mfrom = mo['From']

    if mo.getheader('Bcc'):
        mo.__delitem__('Bcc')

    if not mo.getheader('Date'):
        mo['Date'] = DateTime().rfc822()

    mo.rewindbody()
    finalmessage = mo
    finalmessage = mo.__str__() + '\n' + mfile.read()
    mfile.close()
    return finalmessage, mto, mfrom

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
    item.setFormat('structured-text')
    item._edit(text)

    if Creator:
        if hasattr(item, 'addCreator'):
            item.addCreator(Creator)
        else:
            item.creator = Creator

    pm = getToolByName(self, 'portal_membership')

    if pm.isAnonymousUser():
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

"""
try:
    from Products.MailHost import MailHost
    MailHost._mungeHeaders = _mungeHeaders
except ImportError:
    pass
"""
