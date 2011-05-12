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

    # BBB: Remove skin layers. Need for plone < 3.1
    skin_tool = getToolByName(self, 'portal_skins')
    for skin in skin_tool.getSkinSelections():
        path = [elem for elem in skin_tool.getSkinPath(skin).split(',')]
        for layer in ['captchas_discussion', 'captchas_sendto_form',
                      'captchas_join_form']:
            if layer in skin_tool.objectIds():
                skin_tool.manage_delObjects(ids=[layer])
            if layer in path:
                path.remove(layer)
        skin_path = ','.join(path)
        skin_tool.addSkinSelection(skin, skin_path)
    transaction.savepoint()
