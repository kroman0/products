from types import UnicodeType
from Acquisition import aq_inner

from Products.CMFCore.utils import getToolByName

from MemberdataHandlers import registerMemberdataHandler, IMemberdataHandler

class CMFMemberdataHandler:
    """
        Manage portal_memberdata after migration it to CMFMembers' portal_memberdata tool
    """

    __implements__ = IMemberdataHandler

    def __init__(self, context):
        self.context = context
        self.tool = getToolByName(self.context, 'portal_memberdata')
        self.fieldnames = []
        self.compatible = 'BaseBTreeFolder' in [klass.__name__ for klass in self.tool.__class__.__bases__]
        self.is_compatible()

    def is_compatible(self):
        """
            Take portal_memberdata tool and analyse possibility of working
            with it.
            If handler does not know how to work with given portal_memberdata,
            it return 'False' on init, otherwise - 'True'.
            As condition used inheritance from 'BaseBTreeFolder' class.
        """
        if not self.compatible:
                raise
        return self.compatible

    def listAllMemberProperties(self, exclude_props=[], include_props=None):
        """
            Collect and return all distinct shema fields from all portal cmf members
        """
        if not self.is_compatible(): return []
        all_props = []
        for member in self.getAllMembers():
            if hasattr(aq_inner(member), 'Schema') and callable(member.Schema):
                schema = member.getSchema()
                fields = [f.getName() for f in schema.filterFields()
                    if (f.getName() not in exclude_props) and (include_props and f.getName() in include_props or not include_props)]
                for field in fields:
                    if field not in all_props:
                        all_props.append(str(field))
        return all_props                                                                                    

    def getAllMembers(self):
        """
            Return all members with portal_memberdata.contentValues() folderish method
        """
        if not self.compatible: return []
        return self.tool.contentValues()

    def getMemberProperties(self, member, exclude_props=[], include_props=None):
        """
            Return all needed members' properties as dictionary
            {property name : property value, ...},
            exclude properties from exclue_props parameter.
            Get properties from schemas of every member object and collect it.
        """
        if not self.compatible: return {}
        if hasattr(aq_inner(member), 'Schema') and callable(member.Schema):
            schema = member.getSchema()
            fields = [f.getName() for f in schema.filterFields()
                if (f.getName() not in exclude_props) and (include_props and f.getName() in include_props or not include_props)]
            for field in fields:
                if field not in self.fieldnames:
                    self.fieldnames.append(str(field))
        props = {}
        for field in self.fieldnames:
            value = member.getProperty(str(field), '')
            if type(value) is UnicodeType:
                value = value.encode('UTF8')
            props[field] = value
        return props

registerMemberdataHandler(CMFMemberdataHandler)