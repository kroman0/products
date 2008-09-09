#
# PingTool TestCase
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from base import *

class TestPingTool(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.ptool = self.portal._getOb(TOOL_ID)
        self.portal.invokeFactory('Weblog', id='b1',title='Blog 1')
        self.b1 = getattr(self.portal, 'b1', None)
        self.b1.enableSyndication()

    def testPingToolType(self):
        self.failUnless(self.ptool.meta_type==PingTool.PingTool.meta_type)

    def testSetupPing(self):
        obj = self.b1

        # test default ping setup
        status, message = self.ptool.setupPing(context=obj)
        self.failUnless(status=='success')
        self.failUnless(message=='Changes saved.')
        syInfo = getattr(obj, 'syndication_information', None)
        self.failUnless(syInfo.ping_sites==[])
        self.failUnless(syInfo.enable_ping==0)
        
        # test ping setup with disable syndication and ping
        self.b1.disableSyndication()
        status, message = self.ptool.setupPing(context=obj, enable_ping=0, ping_sites=('http://nohost',), REQUEST=None)
        self.failUnless(status=='failed')
        self.failUnless(message=='Syndication is Disabled')
        syInfo = getattr(obj, 'syndication_information', None)
        self.failUnless(syInfo is None)
        
        # test ping setup with enable syndication and ping
        self.b1.enableSyndication()
        status, message = self.ptool.setupPing(context=obj, enable_ping=1, ping_sites=('http://nohost',), REQUEST=None)
        self.failUnless(status=='success')
        self.failUnless(message=='Changes saved.')
        syInfo = getattr(obj, 'syndication_information', None)
        self.failUnless(syInfo.ping_sites==['http://nohost'])
        self.failUnless(syInfo.enable_ping==1)

    def testGetPingProperties(self):
        obj = self.b1
        syInfo = getattr(obj, 'syndication_information', None)
        syInfo.ping_sites = ('http://nohost/1', 'http://nohost/2')
        syInfo.enable_ping = 1
        dic = self.ptool.getPingProperties(obj)
        self.failUnless(tuple(dic['ping_sites'])==('http://nohost/1','http://nohost/2'))
        self.failUnless(dic['enable_ping']==1)

    def testPingFeedReader(self):
        obj = self.b1

        # test with default properties
        status, message = self.ptool.pingFeedReader(obj)
        self.failUnless(status=='failed')
        self.failUnless(message=='Ping is dissabled.')
"""
        # test with customized properties
        self.ptool.invokeFactory(id = 'testsite', type_name = "PingInfo", title = 'www.TESTSITE.com (blog url)', url = 'http://pingsite')
        self.ptool.setupPing(context=obj, enable_ping=1, ping_sites=('testsite',))
        status, message = self.ptool.pingFeedReader(obj)
        self.failUnless(status=='failed')
        self.failUnless(message=='Ping is impossible.Setup canonical_url.')

        # test with customized properties
        status, message = self.ptool.pingFeedReader(obj)
        self.failUnless(status=='success')
        self.failUnless(message=='The servers are pinged.\nReturned message from http://pingsite: The site http://pingsite generated error for plone/b1.')
"""
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPingTool))
    return suite

if __name__ == '__main__':
    framework()

