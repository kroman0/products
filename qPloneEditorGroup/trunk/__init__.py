try:
    from Products.CMFPlone.interfaces import IPloneSiteRoot
    from Products.GenericSetup import EXTENSION
    from Products.GenericSetup import profile_registry
    has_profiles = True
except ImportError:
    has_profiles = False

def initialize(context):
    if has_profiles:
        profile_desc = "Installs Editor role & group."
        profile_registry.registerProfile('default',
                                         'EditorProfile',
                                         profile_desc,
                                         'profiles/default',
                                         'EditorProfile',
                                         EXTENSION,
                                         for_=IPloneSiteRoot)
    else:
        pass

