from zope.interface import Interface, Attribute

class IGAuthInterface(Interface):
    """ Utility, which operate with authentication data,
        stored in Google Data configlet.
    """

    email = Attribute("email", "Get GDocs portal account email.")

    password = Attribute("password", "Get GDocs portal account password.")
