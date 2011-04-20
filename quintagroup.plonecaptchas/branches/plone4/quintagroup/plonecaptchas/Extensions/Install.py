import transaction
from Products.CMFCore.utils import getToolByName
REQUIRED = 'quintagroup.captcha.core'


def install(self):
    qi = getToolByName(self, 'portal_quickinstaller')
    # install required quintagroup.captcha.core product
    # BBB: Need to success installation in Plone<3.1
    #      (with GenericSetup < v1.4.2, where dependency
    #       support was not yet implemented)
    if not REQUIRED in qi.listInstalledProducts():
        qi.installProduct(REQUIRED)
    # install plonecaptchas
    gs = getToolByName(self, 'portal_setup')
    profile = 'profile-quintagroup.plonecaptchas:default'
    gs.runAllImportStepsFromProfile(profile)
    transaction.savepoint()


def uninstall(self):
    portal_setup = getToolByName(self, 'portal_setup')
    profile = 'profile-quintagroup.plonecaptchas:uninstall'
    portal_setup.runAllImportStepsFromProfile(profile, purge_old=False)
    transaction.savepoint()
