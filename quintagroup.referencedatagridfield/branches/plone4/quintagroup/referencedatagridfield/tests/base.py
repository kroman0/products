import unittest

#from zope.testing import doctestunit
#from zope.component import testing
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc

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
        self.loginAsPortalOwner()
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
        self.logout()

    # def createDefaultStructure(self):
    #     if 'layer1' not in self.portal.objectIds():
    #         self.setRoles(['Manager'])
    #         makeContent(self.portal, portal_type='Folder', id='layer1')
    #         self.portal.layer1.setTitle('Layer1')
    #         self.portal.layer1.reindexObject()
    #         makeContent(self.portal.layer1, portal_type='Folder', id='layer2')
    #         self.folder = self.portal.layer1.layer2
    #         self.folder.setTitle('Layer2')
    #         self.folder.reindexObject()
    #         self.setRoles(['Member'])
    #     return self.portal.layer1.layer2

    # def removeDefaultStructure(self):
    #     if 'layer1' in self.portal.objectIds():
    #         self.portal._delObject('layer1')


class TestCase(MixIn, ptc.PloneTestCase):
    """ Base TestCase for quintagroup.referencedatagridfield """
