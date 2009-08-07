# -*- coding: utf-8 -*-
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

ZOPE_DEPS = []
PLONE_INSTALL = ['QuillsEnabled', 'AutocompleteWidget', 
                 'quintagroup.plonecomments', 'quintagroup.quills.extras']
PLONE_DEPS = ['QuillsEnabled', 'AutocompleteWidget']

@onsetup
def setup_quillsextras_policy():
    """The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    # Load the ZCML configuration for the quintagroup.quills.extras package
    # and its dependencies
    fiveconfigure.debug_mode = True
    import quintagroup.plonecomments
    import quintagroup.quills.extras
    zcml.load_config('configure.zcml', quintagroup.plonecomments)
    zcml.load_config('overrides.zcml', quintagroup.plonecomments)
    zcml.load_config('configure.zcml', quintagroup.quills.extras)
    zcml.load_config('overrides.zcml', quintagroup.quills.extras)
    fiveconfigure.debug_mode = False

    ztc.installPackage('quintagroup.plonecomments')

for p in PLONE_INSTALL:
    ztc.installProduct(p)

setup_quillsextras_policy()
ptc.setupPloneSite(products=PLONE_INSTALL)
