# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2005-11-23 13:47:40 +0200 (Thu, 23 Nov 2005) $
# Copyright: quintagroup.com

"""This module contains class that tests short message """

from Testing import ZopeTestCase
from Products.Archetypes.tests import ArchetypesTestCase
from Products.CMFCore.utils import getToolByName
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Products.PloneTestCase.setup import setupPloneSite

ZopeTestCase.installProduct('ShortMessage')
ZopeTestCase.installProduct('CMFMember')
ZopeTestCase.installProduct('PloneSMSCommunicator')
from Products.ShortMessage import ShortMessage
import time

tests=[]
PRODUCTS=('ShortMessage', 'CMFMember', 'PloneSMSCommunicator')

class TestShortMessage(ArchetypesTestCase.ArcheSiteTestCase):

    def createManager(self, portal):
        acl_users = portal.acl_users
        return acl_users._doAddUser('PortalManager', '', ['Manager'], (), (), )

    def installProducts(self, portal):
        #create manager user
        self.createManager(portal)
        user = portal.acl_users.getUserById('PortalManager')
        #login as manager
        newSecurityManager(None, user)
        #install products
        qi = getToolByName(portal, 'portal_quickinstaller')
        for product in PRODUCTS:
            qi.installProduct(product)
        #log out
        noSecurityManager()

    def afterSetUp(self):

        #get Portal and acl_users
        portal = self.portal
        acl_users = portal.acl_users
        self.installProducts(portal)
        #create ShortMessage object
        us = acl_users.getUserById('PortalManager')
        newSecurityManager(None, us)
        self.folder.invokeFactory(type_name='ShortMessage', id='sms')
        noSecurityManager()


    def test_sender(self):
        self.folder.sms.setSender('+380979312198')
        self.assertEqual(self.folder.sms.getSender(), '+380979312198')

    def test_recipient(self):
        self.folder.sms.setRecipient('g1')
        self.assertEqual(self.folder.sms.getRecipient(), 'g1')

    def test_body(self):
        self.folder.sms.setBody('hello Taras this is text message')
        self.assertEqual(self.folder.sms.getBody(), 'hello Taras this is text message')

tests.append(TestShortMessage)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestShortMessage))
    return suite

if __name__ == '__main__':
    framework()