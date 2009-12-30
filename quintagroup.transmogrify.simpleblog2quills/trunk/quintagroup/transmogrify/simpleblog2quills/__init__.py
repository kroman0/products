# register our extension profile if we have GenericSetup (Plone 2.5 or later)
try:
    # if we have GenericSetup product we don't need to register steps in python
    import os
    from Products.GenericSetup import EXTENSION
    from Products.GenericSetup import profile_registry
    from Products.CMFPlone.interfaces import IPloneSiteRoot

    profile_path = os.path.join(os.path.split(__file__)[0], 'profiles/default')
    profile_registry.registerProfile(
        name="default",
        title="quintagroup.transmogrify.simpleblog2quills (enables Large Plone Folder)",
        description="Extension profile for applying settings needed to migrate blog.",
        path=profile_path,
        product="quintagroup.transmogrify.simpleblog2quills", # this is required
        profile_type=EXTENSION,
        for_=IPloneSiteRoot
    )

except ImportError:
    pass
