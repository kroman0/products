import unittest
import transaction

from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase import setup as ptc_setup
from Products.PloneTestCase.layer import PloneSite
import quintagroup.analytics
ptc.setupPloneSite()

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             quintagroup.analytics)
            fiveconfigure.debug_mode = False
            ztc.installPackage('quintagroup.analytics')
            app = ztc.app()
            portal = app[ptc_setup.portal_name]

            # Sets the local site/manager
            ptc_setup._placefulSetUp(portal)

            qi = getattr(portal, 'portal_quickinstaller', None)
            qi.installProduct('quintagroup.analytics')
            transaction.commit()

        @classmethod
        def tearDown(cls):
            pass


#TO DO:=====================================================================
#      add test to verify if QA control panel action is present;
#      add tests for views registration;
#      add tests for every views methods;
#      add doc tests to validate if all needed elements are present on page;



class TestQAInstallation(TestCase):
    """ This class veryfies registrations of all needed views and
        actions.
    """

    def test_cp_action_installation(self):
        """Here we are testin control panel action. """
        control_panel = self.portal.portal_controlpanel
        self.assert_('QAnalytics' in [a.id for a in control_panel.listActions()],
                     "Configlet for quintagroup.analitycs isn't registered.")


def test_suite():
    from unittest import TestSuite, makeSuite

    test_suite = unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='quintagroup.contentstats',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='quintagroup.contentstats.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='quintagroup.contentstats',
        #    test_class=TestCase),

        #ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='quintagroup.contentstats',
        #    test_class=TestCase),

        ])

    test_suite.addTest(makeSuite(TestQAInstallation))
    return test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
