from Products.CMFCore.utils import getToolByName

from Products.%(product_name)s.config import GS_INSTALL_PROFILE
from Products.%(product_name)s.config import GS_AFTERINSTALL_PROFILE
from Products.%(product_name)s.config import GS_UNINSTALL_PROFILE
from Products.%(product_name)s.config import GS_AFTERINSTALL_STEPS


def install(self, reinstall=False):
    """ Install skin with GenericSetup install profile
    """
    ps = getToolByName(self, 'portal_setup')
    (ps.aq_base).__of__(self).runAllImportStepsFromProfile(GS_INSTALL_PROFILE)

def afterInstall(self, reinstall, product):
    """ Install zexp objects and other dependent objects.
        Perform this step here for prevent removing objects on uninstallation.
    """
    ps = getToolByName(self, 'portal_setup')
    for step in GS_AFTERINSTALL_STEPS:
        (ps.aq_base).__of__(self).runImportStepFromProfile(
             profile_id=GS_AFTERINSTALL_PROFILE, step_id = step,
             run_dependencies=False)

def uninstall(self, reinstall=False):
    """ Uninstall skin with GenericSetup uninstall profile
    """
    ps = getToolByName(self, 'portal_setup')
    (ps.aq_base).__of__(self).runAllImportStepsFromProfile(GS_UNINSTALL_PROFILE)
    
