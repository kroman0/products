from Products.CMFCore.utils import getToolByName

def getCanonicalURL(context):
    """ Uniform method for get portal canonical url."""
    p_url = getToolByName(context, 'portal_url')
    canonical_url = ""
    try:
        from adapter import ICanonicalURL
        canonical_url = ICanonicalURL(p_url).getCanonicalURL()
    except:
        canonical_url = p_url.getCanonicalURL()

    return canonical_url