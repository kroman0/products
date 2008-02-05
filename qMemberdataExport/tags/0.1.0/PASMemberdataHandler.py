from types import UnicodeType

from Products.CMFCore.utils import getToolByName

from MemberdataHandlers import registerMemberdataHandler, IMemberdataHandler
from Products.PluggableAuthService.interfaces.authservice import IPluggableAuthService

class PASMemberdataHandler:
    """
        Manage standard portal_memberdata and portal_membership tools
    """

    __implements__ = IMemberdataHandler

    def __init__(self, context):
        self.context = context
        self.tool = getToolByName(self.context, 'portal_membership', None)
        self.fieldnames = []
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
        all_props = set([])
        for member in self.getAllMembers():
            user = member.getUser()
            for sheet in user.getOrderedPropertySheets():
                all_props = all_props | set(sheet.propertyIds())

        # property sheet hasn't id property, next we add it manually
        all_props = (all_props | set(['id'])) - set(exclude_props)
        if include_props: all_props = all_props & set(include_props)
        return list(all_props)

    def getAllMembers(self):
        """
            Return all members with portal_membership.listMembers() method
        """
        if not self.is_compatible(): return []
        return self.tool.listMembers()

    def getMemberProperties(self, member, exclude_props=[], include_props=None):
        """
            Return all needed members' properties as dictionary
            {property name : property value, ...},
            exclude properties from exclue_props parameter.
            Get properties from portal_memberdata property sheet.
        """
        if not self.is_compatible: return {}
        props = {}
        user = member.getUser()
        for sheet in user.getOrderedPropertySheets():
            for item in sheet.propertyItems():
                field = item[0]
                value = item[1]
                if type(value) is UnicodeType:
                    value = value.encode('UTF8')
                if not props.has_key(field): props[field] = value
        #id property isn't stored in property sheet, we can get it from member or user object
        props['id'] = member.getProperty('id')
        return props

registerMemberdataHandler(PASMemberdataHandler)