from types import UnicodeType
from Acquisition import aq_inner

from Products.CMFCore.utils import getToolByName

from MemberdataHandlers import registerMemberdataHandler, IMemberdataHandler

class RememberMemberdataHandler:
    """
        Manage remember's members
    """

    __implements__ = IMemberdataHandler

    def __init__(self, context):
        self.context = context
        self.tool = getToolByName(self.context, 'portal_memberdata')
        self.membrane_tool = getToolByName(self.context, 'membrane_tool', None)
        self.fieldnames = []
        # for compatibility with Plone 2.0 (import next only on instance init)
        from Products.PluggableAuthService.interfaces.authservice import IPluggableAuthService
        from Products.remember.interfaces import IRememberMembraneTool
        self.compatible = IPluggableAuthService.providedBy(self.context.acl_users) and self.membrane_tool and IRememberMembraneTool.providedBy(self.membrane_tool)
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
            Return all properties from UserPropertySheets and from member's schema.
            Exclude properties that given in exclude_props list.
        """

        if not self.is_compatible(): return []

        for member in self.getAllMembers():
            if hasattr(aq_inner(member), 'Schema') and callable(member.Schema):
                schema = member.getSchema()
                for field in schema.filterFields():
                    fname = str(field.getName())
                    if (fname not in exclude_props) and (include_props and fname in include_props or not include_props):
                        if fname not in self.fieldnames:
                            self.fieldnames.append(fname)

        for member in self.getAllMembers():
            for sheet in member.getOrderedPropertySheets():
                for name in sheet.propertyIds():
                    if (name not in exclude_props) and (include_props and name in include_props or not include_props):
                        if name not in self.fieldnames:
                            self.fieldnames.append(name)

        return self.fieldnames

    def getAllMembers(self):
        """
            Return all members contained in portal_memberdata tool
        """
        if not self.compatible: return []
        return self.tool.contentValues()

    def getMemberProperties(self, member, exclude_props=[], include_props=None):
        """
            Return all needed members' properties as dictionary
            {property name : property value, ...},
            exclude properties from exclue_props parameter.
            Get properties:
            1. from member's schema fields
            2. from PAS, PlonePas (portal_memberdata), Membrane and any else registered UserPropertySheets for member

        """

        if not self.is_compatible: return {}
        props = {}

        # extract all info from member schema
        if hasattr(aq_inner(member), 'Schema') and callable(member.Schema):
            schema = member.Schema()
            for field in schema.filterFields():
                fname = str(field.getName())
                if (fname not in exclude_props) and (include_props and fname in include_props or not include_props):
                    if not props.has_key(fname):
                        value = str(member.getProperty(fname, ''))
                        if type(value) is UnicodeType:
                            value = value.encode('UTF8')
                        props[fname] = value
                    if fname not in self.fieldnames:
                        self.fieldnames.append(fname)

        # extract all info from UserPropertySheets
        user = member.getUser()
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

registerMemberdataHandler(RememberMemberdataHandler)