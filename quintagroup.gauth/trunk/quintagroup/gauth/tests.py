import unittest

#from zope.testing import doctestunit
#from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

import quintagroup.gauth


class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            ztc.installPackage(quintagroup.gauth)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass


# class SafeQuery(object):
#     def safeCall(self, serv, meth, methargs=[], methkwargs={}):
#         print "safecall %s: serv: %s, meth: %s, methargs: %s, methkwargs: %s" % (
#             self, serv, meth, methargs, methkwargs)
#         try:
#             return meth(*methargs, **methkwargs)
#         except gdata.service.RequestError, e:
#             print "Token Expired -> Update it."
#             logException("Token Expired -> Update it.")
#             serv.ProgrammaticLogin()
#             return meth(*methargs, **methkwargs)
# counter = 0
# class DummyServ:
#     def ProgrammaticLogin(self, captcha_token=None, captcha_response=None):
#         print "for '%s' called ProgrammaticLogin" % str(self)
#     def Query(self, *args, **kwargs):
#         global counter
#         if counter > 3:
#             counter = 0
#             raise gdata.service.RequestError("Some Problem in Query")
#         print "for '%s' called Query with args: %s, kwargs: %s" % tuple(
#             map(str,[self,args,kwargs]))
#         counter += 1
# class C(SafeQuery):
#     serv = None
#     def __init__(self):
#         self.serv = DummyServ()
#     def operation(self, a):
#         for i in range(5):
#             self.safeCall(self.serv, self.serv.Query, [i,], {"q": i*i})






def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='quintagroup.gauth',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='quintagroup.gauth.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='quintagroup.gauth',
        #    test_class=TestCase),

        #ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='quintagroup.gauth',
        #    test_class=TestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
