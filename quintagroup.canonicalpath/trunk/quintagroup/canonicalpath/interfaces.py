from zope.interface import Interface, Attribute
from zope.schema import URI

class ICanonicalPath(Interface):
    """canonical_path provider interface
    """

    # canonical_path = URI(
    #     title=u"canonical_path",
    #     description = u"canonical_path - for the object. Adapter must " \
    #                   u"implement *setter* and *getter* for the attribute")

    canonical_path = Attribute("canonical_path",
        "canonical_path - for the object. Adapter must implement "
        "*setter* and *getter* for the attribute")

