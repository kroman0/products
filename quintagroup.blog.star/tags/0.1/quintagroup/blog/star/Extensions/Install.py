import logging
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('quintagroup.blog.star')

def uninstall(portal, reinstall=False):
    """ Uninstall this product.

        This external method is need, because portal_quickinstaller doens't know
        what GenericProfile profile to apply when uninstalling a product.
    """
    setup_tool = getToolByName(portal, 'portal_setup')
    if reinstall:
        return "Ran all reinstall steps."
    else:
        setup_tool.runAllImportStepsFromProfile('profile-quintagroup.blog.star:uninstall')
        return "Ran all uninstall steps."
