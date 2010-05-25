from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.upgrade import _upgrade_registry

PROFILE = "profile-quintagroup.plonegooglesitemaps:default"

def install(self, reinstall=False):
    """ Install skin with GenericSetup install profile
    """
    ps = getToolByName(self, 'portal_setup')
    mtool = getToolByName(self, 'portal_migration')
    plone_version = mtool.getFileSystemVersion()
    isPlone3 = plone_version.startswith('3')
    isPlone4 = plone_version.startswith('4')

    if reinstall and (isPlone3 or isPlone4):
        step = None
        profile_id = 'quintagroup.plonegooglesitemaps:default'
        steps_to_run = [s['id'] for s in setup_tool.listUpgrades(profile_id, show_old=False)]
        for step_id in steps_to_run:
            step = _upgrade_registry.getUpgradeStep(profile_id, step_id)
            step.doStep(setup_tool)
            msg = "Ran upgrade step %s for profile %s" % (step.title, profile_id)
            logger.log(logging.INFO, msg)
        # We update the profile version to the last one we have reached
        # with running an upgrade step.
        if step and step.dest is not None and step.checker is None:
           setup_tool.setLastVersionForProfile(profile_id, step.dest)
        return "Ran all reinstall steps."

    if (isPlone3 or isPlone4):
        # if this is plone 3.x
        (ps.aq_base).__of__(self).runAllImportStepsFromProfile(PROFILE)
    else:
        active_context_id = ps.getImportContextID()
        ps.setImportContext(PROFILE)
        ps.runAllImportSteps()
        ps.setImportContext(active_context_id)
