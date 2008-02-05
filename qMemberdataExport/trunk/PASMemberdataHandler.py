from types import UnicodeType

from Products.CMFCore.utils import getToolByName

from MemberdataHandlers import registerMemberdataHandler, IMemberdataHandler

class PASMemberdataHandler:
    """
        Manage standard portal_memberdata and portal_membership tools
    """

    __implements__ = IMemberdataHandler

    def __init__(self, context):
        self.context = context
        self.tool = getToolByName(self.context, 'portal_membership', None)
        self.fieldnames = []
        # for compatibility with Plone 2.0 (import next only on instance init)
        from Products.PluggableAuthService.interfaces.authservice import IPluggableAuthService
        self.compatible = IPluggableAuthService.providedBy(self.context.acl_users)
        self.is_compatible()

    def is_compatible(self):
        """
            Take portal_memberdata tool and analyse possibility of working
            with it.
            If handler does not know how to work with given portal_memberdata,
            it return 'False' on init, otherwise - 'True'.
        """
        if not self.compatible:
            raise
        return self.compatible

    def listAllMemberProperties(self, exclude_props=[], include_props=None):
        """
            Return all properties from portal_memberdatas' property sheet.
            Exclude properties that given in exclude_props list.
        """
        if not self.is_compatible(): return []

        if ('id' not in exclude_props) and (include_props and 'id' in include_props or not include_props):
            if 'id' not in self.fieldnames: self.fieldnames.append('id')
        for memberId in self.getAllMembers():
            user = self.tool.acl_users.getUserById(memberId)
            for sheet in user.getOrderedPropertySheets():
                for name in sheet.propertyIds():
                    if (name not in exclude_props) and (include_props and name in include_props or not include_props):
                        if name not in self.fieldnames: self.fieldnames.append(name)

        return self.fieldnames

    def getAllMembers(self):
        """
            Return all members with portal_membership.listMembers() method
            (now this method returns only member ids)
        """
        if not self.is_compatible(): return []
        mid_list = [user['userid'] for user in self.tool.acl_users.searchUsers()]

        return mid_list

    def getMemberProperties(self, member, exclude_props=[], include_props=None):
        """
            Return all needed members' properties as dictionary
            {property name : property value, ...},
            exclude properties from exclue_props parameter.
            Get properties from portal_memberdata property sheet.
        """

        if not self.is_compatible: return {}
        props = {}
        # manually set id
        if ('id' not in exclude_props) and (include_props and 'id' in include_props or not include_props):
            if not props.has_key('id'): props['id'] = member
            if 'id' not in self.fieldnames: self.fieldnames.append('id')
        user = self.tool.acl_users.getUserById(member)
        for sheet in user.getOrderedPropertySheets():
            for field, value in sheet.propertyItems():
                if type(value) is UnicodeType:
                    value = value.encode('UTF8')
                if (field not in exclude_props) and (include_props and field in include_props or not include_props):
                    if not props.has_key(field):
                        props[field] = value
                    if field not in self.fieldnames:
                        self.fieldnames.append(str(field))

        return props

registerMemberdataHandler(PASMemberdataHandler)