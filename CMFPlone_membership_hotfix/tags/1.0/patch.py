from Products.CMFCore.CMFCorePermissions import SetOwnPassword
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.MembershipTool import MembershipTool as BaseTool
from Products.CMFPlone import ToolNames
from Products.CMFPlone.PloneUtilities import translate
from Products.CMFPlone.PloneUtilities import _createObjectByType
from OFS.Image import Image
from AccessControl import ClassSecurityInfo, getSecurityManager
from Globals import InitializeClass
from Acquisition import aq_base, aq_parent, aq_inner
from Products.CMFCore.CMFCorePermissions import View
from Products.CMFPlone.PloneBaseTool import PloneBaseTool

from utils import scale_image
from Globals import InitializeClass, DTMLFile
from ZODB.POSException import ConflictError
from Products.CMFCore.utils import _checkPermission

from Products.CMFPlone.MembershipTool import MembershipTool
    
def changeMemberPortrait(self, portrait, member_id=None):
    """
    given a portrait we will modify the users portrait
    we put this method here because we do not want
    .personal or portrait in the catalog
    """
    if not member_id:
        member_id = self.getAuthenticatedMember().getUserName()

    if portrait and portrait.filename:
        scaled, mimetype = scale_image(portrait)
        portrait = Image(id=member_id, file=scaled, title='')
        membertool   = getToolByName(self, 'portal_memberdata')
        membertool._setPortrait(portrait, member_id)



def getBadMembers(self):
    """Will search for members with bad images in the portal_memberdata
    delete their portraits and return their member ids"""
    memberdata = getToolByName(self, 'portal_memberdata')
    portraits = getattr(memberdata, 'portraits', None)
    if portraits is None:
        return []
    bad_member_ids = []
    TXN_THRESHOLD = 50
    counter = 1
    for member_id in tuple(portraits.objectIds()):
        portrait = portraits[member_id]
        portrait_data = str(portrait.data)
        if portrait_data == '':
            continue
        try:
            img = PIL.Image.open(StringIO(portrait_data))
        except ConflictError:
            pass
        except:
            # Anything else we have a bad bad image and we destroy it
            # and ask questions later.
            portraits._delObject(member_id)
            bad_member_ids.append(member_id)
        if not counter%TXN_THRESHOLD:               
            get_transaction().commit()
        counter = counter + 1

    return bad_member_ids


def deleteMemberArea(self, member_id):
    """ Delete member area of member specified by member_id.
    """
    members = self.getMembersFolder()
    if not members:
        return 0
    if hasattr( aq_base(members), member_id ):
        members.manage_delObjects(member_id)
        return 1
    else:
        return 0


def deleteMembers(self, member_ids, delete_memberareas=1,
                    delete_localroles=1):
    """ Delete members specified by member_ids.
    """

    # Delete members in acl_users.
    acl_users = self.acl_users
    if _checkPermission('Manage Users', acl_users):
        if isinstance(member_ids, basestring):
            member_ids = (member_ids,)
        member_ids = list(member_ids)
        for member_id in member_ids[:]:
            if not acl_users.getUserById(member_id, None):
                member_ids.remove(member_id)
        try:
            acl_users.userFolderDelUsers(member_ids)
        except (NotImplementedError, 'NotImplemented'):
            raise NotImplementedError('The underlying User Folder '
                                        'doesn\'t support deleting members.')
    else:
        raise AccessControl_Unauthorized('You need the \'Manage users\' '
                                'permission for the underlying User Folder.')

    # Delete member data in portal_memberdata.
    mdtool = getToolByName(self, 'portal_memberdata', None)
    if mdtool is not None:
        for member_id in member_ids:
            members = mdtool._members
            if members.has_key(member_id):
                del members[member_id]

    # Delete members' home folders including all content items.
    if delete_memberareas:
        for member_id in member_ids:
                self.deleteMemberArea(member_id)

    # Delete members' local roles.
    if delete_localroles:
        utool = getToolByName(self, 'portal_url', None)
        self.deleteLocalRoles( utool.getPortalObject(), member_ids,
                                reindex=1 )

    return tuple(member_ids)


MembershipTool.manage_options = (MembershipTool.manage_options +
                      ( { 'label' : 'Portraits'
                     , 'action' : 'manage_portrait_fix'
                     },))
MembershipTool.security = ClassSecurityInfo()
MembershipTool.security.declareProtected('Manage Portal', 'manage_portrait_fix')
MembershipTool.manage_portrait_fix = DTMLFile('www/portrait_fix', globals())
MembershipTool.security.declareProtected('Manage Portal', 'getBadMembers')
MembershipTool.getBadMembers = getBadMembers
MembershipTool.security.declareProtected('Manage Users', 'deleteMemberArea')
MembershipTool.deleteMemberArea = deleteMemberArea
MembershipTool.security.declareProtected('Manage Users', 'deleteMembers')
MembershipTool.deleteMembers = deleteMembers

InitializeClass(MembershipTool)
