from Testing import ZopeTestCase
#from Products.Archetypes.tests import ArchetypesTestCase
from Products.CMFPlone.tests import PloneTestCase
from Products.CMFCore.utils import getToolByName

from Products.PloneSMSCommunicator.pyXIAM import SMSsubmitRequest, getAllTextFromTag
import xml.dom
from xml.dom.minidom import *

ZopeTestCase.installProduct('PloneSMSCommunicator')

tests=[]

class TestpyXIAM(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        portal = self.portal
        sms=SmSsubmitRequest(originator = '+380979312198', destination = ['+380979987348'], body = 'hello how are you?')
        self.doc = sms.toXML()
        self.doc = parseString(self.doc)


    def test_originator(self):
        self.assertEqual(getAllTextFromTag(self.doc, 'from')[0], '+380979312198')

    def test_destination(self):
        self.assertEqual(getAllTextFromTag(self.doc, 'to')[0], '+380979987348')

    def test_content(self):
        self.assertEqual(getAllTextFromTag(self.doc, 'content')[0], 'hello how are you?')


tests.append(TestpyXIAM)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestpyXIAM))
    return suite

if __name__ == '__main__':
    framework()