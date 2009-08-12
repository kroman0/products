# -*- coding: utf-8 -*-
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

ZOPE_DEPS = []

try:
    import quintagroup.plonecomments
except ImportError:
    QPC_PACKAGE = False
    from Products import qPloneComments
else:
    QPC_PACKAGE = True

PLONE_INSTALL = ['QuillsEnabled', 'AutocompleteWidget', 
                 'quintagroup.plonecomments', 'quintagroup.quills.extras']
PLONE_DEPS = ['QuillsEnabled', 'AutocompleteWidget']

if QPC_PACKAGE:
    PLONE_INSTALL += ['quintagroup.plonecomments',]
else:
    PLONE_INSTALL += ['qPloneComments',]
    PLONE_DEPS    += ['qPloneComments',]

@onsetup
def setup_quillsextras_policy():
    """The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    # Load the ZCML configuration for the quintagroup.quills.extras package
    # and its dependencies
    fiveconfigure.debug_mode = True
    import quintagroup.quills.extras
    zcml.load_config('configure.zcml', quintagroup.quills.extras)
    zcml.load_config('overrides.zcml', quintagroup.quills.extras)
    if QPC_PACKAGE:
        import quintagroup.plonecomments
        zcml.load_config('configure.zcml', quintagroup.plonecomments)
        zcml.load_config('overrides.zcml', quintagroup.plonecomments)
        ztc.installPackage('quintagroup.plonecomments')

    fiveconfigure.debug_mode = False


for p in PLONE_INSTALL:
    ztc.installProduct(p)

setup_quillsextras_policy()
ptc.setupPloneSite(products=PLONE_INSTALL)

import patches
