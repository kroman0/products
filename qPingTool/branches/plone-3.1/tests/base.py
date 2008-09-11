from Products.PloneTestCase import PloneTestCase as PloneTestCase

from Products.CMFCore.utils import getToolByName
from Products.Five.testbrowser import Browser

from Products.qPingTool import PingTool
from Products.qPingTool.config import *

PRODUCTS = ['qPingTool', 'Quills']

map(PloneTestCase.installProduct, ('qPingTool', 'XMLRPCMethod', 'Quills'))

PloneTestCase.setupPloneSite(products=PRODUCTS)

class TestCase(PloneTestCase.PloneTestCase):
    """Base class used for test cases
    """

class FunctionalTestCase(PloneTestCase.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """

    def afterSetUp(self):
        super(FunctionalTestCase, self).afterSetUp()

        self.browser = Browser()

        self.uf = self.portal.acl_users
        self.uf.userFolderAddUser('root', 'secret', ['Manager'], [])

        self.ptool = getToolByName(self.portal, 'portal_properties')
        self.pitool = getToolByName(self.ptool, 'portal_pingtool')
        self.site_props = self.ptool.site_properties

    def loginAsManager(self, user='root', pwd='secret'):
        """points the browser to the login screen and logs in as user root with Manager role."""
        self.browser.open('http://nohost/plone/')
        self.browser.getLink('Log in').click()
        self.browser.getControl('Login Name').value = user
        self.browser.getControl('Password').value = pwd
        self.browser.getControl('Log in').click()

