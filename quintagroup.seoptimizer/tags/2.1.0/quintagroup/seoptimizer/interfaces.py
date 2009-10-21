from zope.interface import Interface

class IKeywords(Interface):
    """Handle the available keywords.
    """
    def listKeywords():
        """Returns all the existing keywords for the current content type.
        """

class IMappingMetaTags(Interface):
    """
    """
    def getMappingMetaTags():
        """Returns mapping {meta_name:accssesor} all the meta tags.
        """
