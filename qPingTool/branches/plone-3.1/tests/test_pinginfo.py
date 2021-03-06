#
# PingInfo TestCase
#

from base import *

class TestPingInfo(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.portal.invokeFactory('PingTool', id='pt1',title='Ping Tool 1')
        self.pt1 = getattr(self.portal, 'pt1', None)
        self.pt1.invokeFactory('PingInfo', id='pi1',title='Ping Info 1')
        self.pi1 = getattr(self.pt1, 'pi1', None)

    def testAddedPingInfo(self):
        self.pi1.setUrl('http://nohost')
        self.failUnlessEqual(self.pi1.getUrl(), 'http://nohost')
        self.failUnlessEqual(self.pi1.getMethod_name(), 'weblogUpdates.ping')
        self.pi1.setMethod_name('testmethod')
        self.failUnlessEqual(self.pi1.getMethod_name(), 'testmethod')        
        self.pi1.setRss_version(self.pi1.Vocabulary('rss_version')[0][-1])
        self.failUnlessEqual(self.pi1.getRss_version(), 'RSS2')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPingInfo))
    return suite
