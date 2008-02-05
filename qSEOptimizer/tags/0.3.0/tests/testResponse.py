#
# Test product functionality
#

import os, sys, string
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from Products.CMFCore.utils import getToolByName
from Products.CMFQuickInstallerTool.InstalledProduct import InstalledProduct
from Products.CMFCore.CMFCorePermissions import ManagePortal

class TestResponse(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
	data = self.publish(self.portal.id+'/front-page/qseo_properties_edit?title=Hello&title_override=1','mgr:mgrpw', env=None, extra= None ,stdin = out)

    def testChangeTitle(self):
	self.assertEqual('Hello', 'Hello')
    
    def testDescriptionTag(self):
	pass
	
    def testKeywordsTag(self):
	pass

    def testHTMLComments(self):
	pass
	
    def testRobotTag(self):
	pass

    def testDistributionTag(self):
	pass

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestResponse))
    return suite

if __name__ == '__main__':
    framework()

