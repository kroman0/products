# this module is needed for backward compatibility with old Plone 2.1
# here we try to import some interfaces and if ImportError is raised
# define it manually

from zope.interface import Interface
from zope.interface import implements

# next are used in atschemaupdater.py

try:
    from Products.Archetypes.interfaces import IBaseObject
except ImportError:
    class IBaseObject(Interface):
        """ The most basic Archetypes-based implementation
        """

try:
    from Products.Archetypes.event import ObjectInitializedEvent
    from Products.Archetypes.event import ObjectEditedEvent
except ImportError:
    from zope.app.event.interfaces import IObjectModifiedEvent
    from zope.app.event.objectevent import ObjectModifiedEvent

    class IObjectInitializedEvent(IObjectModifiedEvent):
        """An object is being initialised, i.e. populated for the first time
        """

    class IObjectEditedEvent(IObjectModifiedEvent):
        """An object is being edited, i.e. modified after the first save
        """

    class ObjectInitializedEvent(ObjectModifiedEvent):
        """An object is being initialised, i.e. populated for the first time
        """
        implements(IObjectInitializedEvent)

    class ObjectEditedEvent(ObjectModifiedEvent):
        """An object is being edited, i.e. modified after the first save
        """
        implements(IObjectEditedEvent)

# next is used in browserdefault.py

try:
    from Products.CMFDynamicViewFTI.interface import ISelectableBrowserDefault
except ImportError:
    class ISelectableBrowserDefault(Interface):
        """Content supporting operations to explicitly set the default layout 
        template or default page object.
        """

# next is used in criteria.py

try:
    from Products.ATContentTypes.interface import IATTopic
except ImportError:
    # ATContentTypes creates bridge interfaces, but they are created later
    # from Products.ATContentTypes.z3.interfaces import IATTopic
    class IATTopic(Interface):
        """AT Topic marker interface
        """
