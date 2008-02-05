# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2006-08-11 
# Copyright: quintagroup.com

from __future__ import nested_scopes

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))


"""This module contains class that tests ruid_to_url transformation """

from Testing import ZopeTestCase
from Products.Archetypes.tests.atsitetestcase import ATSiteTestCase

from Products.qPloneResolveUID.transforms.ruid_to_url import ruid_to_url
from Products.qPloneResolveUID.tests.test_data import *

ZopeTestCase.installProduct('qPloneResolveUID')
import time

tests=[]
PRODUCTS=('qPloneResolveUID',)



class TransformTest(ATSiteTestCase):
    
    def afterSetUp(self):
        ATSiteTestCase.afterSetUp(self)
        self.loginAsPortalOwner()
        for product in PRODUCTS:
            self.addProduct(product)
        self.pt = self.portal.portal_transforms    
    
    def test_qPloneResolveUIDInstallation(self):
        qi = self.portal.portal_quickinstaller
        self.assert_('qPloneResolveUID' in [prod['id']for prod in qi.listInstalledProducts()], 
                     "qPloneResolveUID doesn't installed"   
                    )
    
    def test_ruid_to_url_registration(self):
        self.assert_('ruid_to_url' in self.pt.objectIds(), 
                     "ruid_to_url transformation not registered"
                    )
    def test_polisy_registration(self):
        self.assert_(('text/x-html-safe', ('ruid_to_url',)) in self.pt.listPolicies(),
                     'Policy for text/x-html-safe mimetype is not installed'
                    )
    
    def test_ruid_to_url(self):
        if not 'test1' in self.portal.objectIds():
            self.portal.invokeFactory('Folder', 'test1')
        test1 = getattr(self.portal, 'test1', None)
        if test1:
            test1_uid = test1.UID()
            test1.invokeFactory('Document', 'test2')
            test2 = getattr(test1, 'test2', None)
            if test2:
                test2_uid = test2.UID()
        self.assertEqual(self.pt.convert('ruid_to_url',
                                         orig_text %(test1_uid, test2_uid),
                                         context = self.portal
                                        ).getData(),
                         result
                        )
                     
    
tests.append(TransformTest)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TransformTest))
    return suite

if __name__ == '__main__':
    framework()