import unittest

#from zope.testing import doctestunit
#from zope.component import testing
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager

from Products.Archetypes.tests.utils import makeContent

from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

# install site
ptc.setupPloneSite(extension_profiles=[
        'quintagroup.referencedatagridfield:default',
        'quintagroup.referencedatagridfield:examples'
        ])

import quintagroup.referencedatagridfield

class MixIn(object):
    """ Mixin for setting up the necessary bits for testing the
        quintagroup.referencedatagridfield
    """

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             quintagroup.referencedatagridfield)
            ztc.installPackage('quintagroup.referencedatagridfield')
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

    def createDemo(self):
        # Create tested content
        sm = getSecurityManager()
        self.loginAsPortalOwner()
        try:
            if not 'demo' in self.portal.objectIds():
                makeContent(self.portal, portal_type='ReferenceDataGridDemoType', id='demo')
                self.demo = self.portal.demo
                self.demo.setTitle('Reference DataGrid Field Demo')
                self.demo.reindexObject()
            if not 'doc' in self.portal.objectIds():
                makeContent(self.portal, portal_type='Document', id='doc')
                self.doc = self.portal.doc
                self.doc.setTitle('Test Document')
                self.doc.reindexObject()
        finally:
            setSecurityManager(sm)

class TestCase(MixIn, ptc.PloneTestCase):
    """ Base TestCase for quintagroup.referencedatagridfield """
