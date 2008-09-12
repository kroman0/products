#
# PingInfo TestCase
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from base import *

class TestPingTool(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.ptool = self.portal._getOb(TOOL_ID)
        self.portal.invokeFactory('Blog', id='b1',title='Blog 1')
        self.b1 = getattr(self.portal, 'b1', None)
        self.b1.enableSyndication()

    def testPingToolType(self):
        self.failUnless(self.ptool.meta_type==PingTool.PingTool.meta_type)

    def testAddedPingTool(self):
        self.portal.invokeFactory('PingTool', id='pt1',title='Ping Tool 1')
        self.pt1 = getattr(self.portal, 'pt1', None)
        self.failUnless(self.pt1.meta_type==PingTool.PingTool.meta_type)
        self.failUnless(self.pt1.title=='Ping Tool 1')

    def testSetupPing(self):
        obj = self.b1

        # test default ping setup
        status, message = self.ptool.setupPing(context=obj)
        self.failUnless(status=='success')
        self.failUnless(message=='Your changes have been saved')
        syInfo = getattr(obj, 'syndication_information', None)
        self.failUnless(syInfo.ping_sites==[])
        self.failUnless(syInfo.enable_ping==0)
        
        # test ping setup with disable syndication and ping
        self.b1.disableSyndication()
        
        status, message = self.ptool.setupPing(context=obj, enable_ping=0, ping_sites=('http://nohost',), REQUEST=None)
        self.failUnless(status=='failed')
        self.failUnless(message=='Syndication is Disabled')
        syInfo = getattr(obj, 'syndication_information', None)
        self.failUnless(syInfo==None)
        
        # test ping setup with enable syndication and ping
        self.b1.enableSyndication()
        status, message = self.ptool.setupPing(context=obj, enable_ping=1, ping_sites=('http://nohost',), REQUEST=None)
        self.failUnless(status=='success')
        self.failUnless(message=='Your changes have been saved')
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

    def testPingFeedReaderDefault(self):
        obj = self.b1
        # test with default properties
        status, message = self.ptool.pingFeedReader(obj)
        self.failUnless(status=='failed')
        self.failUnless(message=='Ping is impossible.See portal_pingtool.')

    def testPingFeedReaderCustomization(self):
        obj = self.b1
        # test with customization properties
        self.ptool.invokeFactory(id = 'testsite', type_name = "PingInfo", title = 'www.TESTSITE.com (blog url)', url = 'http://nohost/')
        self.ptool.setupPing(context=obj, enable_ping=1, ping_sites=('testsite',))
        self.failUnless(self.portal.getProperty('canonical_url', None) is None)
        self.portal.manage_addProperty('canonical_url', 'localhost', 'string')
        self.failUnless(self.portal.getProperty('canonical_url', None) == 'localhost')
        status, message = self.ptool.pingFeedReader(obj)
        self.failUnless(status=='success')
        self.failUnless(message=='The servers are pinged\nNone')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPingTool))
    return suite

if __name__ == '__main__':
    framework()

