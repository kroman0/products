try:
    from Interface import Interface
except ImportError:
    # for Zope versions before 2.6.0
    from Interface import Base as Interface

_memberdata_handlers = []

def registerMemberdataHandler(klass):

    if not klass in _memberdata_handlers:
        _memberdata_handlers.insert(0, klass)

def unregisterMemberdataHandler(klass):

    if klass in _memberdata_handlers:
        _memberda_handlers.remove(klass)

def getRegisteredMemberdataHandlers():

    return _memberdata_handlers

class IMemberdataHandler(Interface):
    """
        Manage portal_memberdata and return needed information
    """

    def is_compatible(memberdata_tool):
        """
            Take portal_memberdata tool and analyse possibility of working
            with it.
            If handler does not know how to work with given portal_memberdata,
            it raise an exception on init.
        """

    def listAllMemberProperties(exclude_props=[], include_props=None):
        """
            Return all properties that can have any member in portal
        """

    def getAllMembers():
        """
            Return all members appropriate to the given portal_memberdata
        """

    def getMemberProperties(member, exclude_props=[], include_props=None):
        """
            Return all needed members' properties as dictionary
            {property name : property value, ...},
            exclude properties from exclue_props parameter
        """
