from types import UnicodeType

from Products.CMFCore.utils import getToolByName

from MemberdataHandlers import registerMemberdataHandler, IMemberdataHandler

class BaseMemberdataHandler:
    """
        Manage standard portal_memberdata and portal_membership tools
    """

    __implements__ = IMemberdataHandler

    def __init__(self, context):
        self.context = context
        self.tool = getToolByName(self.context, 'portal_memberdata')
        self.fieldnames = []
        self.compatible = True
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
        return [prop for prop in ['id',] + self.tool.propertyIds()
                   if (prop not in exclude_props) and (include_props and prop in include_props or not include_props)]

    def getAllMembers(self):
        """
            Return all members with portal_membership.listMembers() method
        """
        if not self.is_compatible(): return []
        mtool = getToolByName(self.context, 'portal_membership')
        return mtool.listMembers()

    def getMemberProperties(self, member, exclude_props=[], include_props=None):
        """
            Return all needed members' properties as dictionary
            {property name : property value, ...},
            exclude properties from exclue_props parameter.
            Get properties from portal_memberdata property sheet.
        """
        if not self.is_compatible: return {}
        self.fieldnames = self.listAllMemberProperties(exclude_props=exclude_props, include_props=include_props)
        props = {}
        for field in self.fieldnames:
            value = member.getProperty(field, '')
            if type(value) is UnicodeType:
                value = value.encode('UTF8')
            props[field] = value
        return props

registerMemberdataHandler(BaseMemberdataHandler)