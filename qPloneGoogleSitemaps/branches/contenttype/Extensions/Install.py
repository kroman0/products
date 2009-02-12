from Products.CMFCore.utils import getToolByName

def install(self, reinstall=False):
    """ Install skin with GenericSetup install profile
    """
    ps = getToolByName(self, 'portal_setup')
    mtool = getToolByName(self, 'portal_migration')
    plone_version = mtool.getFileSystemVersion()

    if plone_version.startswith('3'):
        # if this is plone 3.x
        (ps.aq_base).__of__(self).runAllImportStepsFromProfile("profile-Products.qPloneGoogleSitemap:default")
    else:
        active_context_id = ps.getImportContextID()
        ps.setImportContext("Products.qPloneGoogleSitemap:default")
        ps.runAllImportSteps()
        ps.setImportContext(active_context_id)
