import unittest
import transaction

from AccessControl.SecurityManagement import newSecurityManager
from zope.component import testing, queryMultiAdapter
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase import setup as ptc_setup
from Products.PloneTestCase.layer import PloneSite
import quintagroup.analytics
ptc.setupPloneSite()

class Installed(PloneSite):

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

class SetUpContent(Installed):

    max = 10
    types_ = ['Document', 'Event', 'Folder']
    users = [('user%s'%i, 'user%s'%i, 'Member', None)
             for i in xrange(max)]

    @classmethod
    def setupUsers(cls, portal):
        """ Creates users."""
        acl_users = portal.acl_users
        mp = portal.portal_membership
        map(acl_users._doAddUser, *zip(*cls.users))
        if not mp.memberareaCreationFlag:
            mp.setMemberareaCreationFlag()
        map(mp.createMemberArea, [u[0] for u in cls.users])

    @classmethod
    def setupContent(cls, portal):
        """ Creates users"""
        uf = portal.acl_users
        pm = portal.portal_membership
        pc = portal.portal_catalog
        users = [u[0] for u in cls.users]
        for u in users:
            folder = pm.getHomeFolder(u)
            user = uf.getUserById(u)
            if not hasattr(user, 'aq_base'):
                user = user.__of__(uf)
            newSecurityManager(None, user)
            for i in xrange(users.index(u)+cls.max):
                map(folder.invokeFactory, cls.types_, [t+str(i) for t in cls.types_])
        transaction.commit()


    @classmethod
    def setUp(cls):
        app = ztc.app()
        portal = app[ptc_setup.portal_name]
        cls.setupUsers(portal)
        cls.setupContent(portal)

    @classmethod
    def tearDown(cls):
        pass

class TestCase(ptc.PloneTestCase):
    layer = Installed

#TO DO:=====================================================================
#      add tests for every views methods;
#      add doc tests to validate if all needed elements are present on page;

class TestQAInstallation(TestCase):
    """ This class veryfies registrations of all needed views and
        actions.
    """

    def test_cp_action_installation(self):
        """This test validates control panel action. """
        control_panel = self.portal.portal_controlpanel
        self.assert_('QAnalytics' in [a.id for a in control_panel.listActions()],
                     "Configlet for quintagroup.analitycs isn't registered.")

    def test_OwnershipByType(self):
        """ This test validates registration of
            ownership_by_type view.
        """
        view = queryMultiAdapter((self.portal, self.portal.REQUEST),
                                 name="ownership_by_type")

        self.assert_(view, "Ownership by type view isn't registered")

    def test_OwnershipByState(self):
        """ This test validates registration of
            ownership_by_state view.
        """
        view = queryMultiAdapter((self.portal, self.portal.REQUEST),
                                 name="ownership_by_state")

        self.assert_(view, "Ownership by state view isn't registered")

    def test_TypeByState(self):
        """ This test validates registration of
            type_by_state view.
        """
        view = queryMultiAdapter((self.portal, self.portal.REQUEST),
                                 name="type_by_state")

        self.assert_(view, "Type by state view isn't registered")

    def test_LegacyPortlets(self):
        """ This test validates registration of
            legacy_portlets view.
        """
        view = queryMultiAdapter((self.portal, self.portal.REQUEST),
                                 name="legacy_portlets")

        self.assert_(view, "Legacy Portlets view isn't registered")

    def test_PropertiesStats(self):
        """ This test validates registration of
            properties_stats view.
        """
        view = queryMultiAdapter((self.portal, self.portal.REQUEST),
                                 name="properties_stats")

        self.assert_(view, "Properties Stats view isn't registered")


    def test_PortletsStats(self):
        """ This test validates registration of
            portlets_stats view.
        """
        view = queryMultiAdapter((self.portal, self.portal.REQUEST),
                                 name="portlets_stats")

        self.assert_(view, "Portlets Stats view isn't registered")

class TestOwnershipByType(TestCase):
    """Tests all ownership by type view methods."""

    layer = SetUpContent

    def test_getUsers(self):
        """
        """
        view = queryMultiAdapter((self.portal, self.portal.REQUEST),
                                 name="ownership_by_type")

        self.assert_(False in map(lambda u1, u2:u1==u2,
                     [u[0] for u in self.layer.users], view.getUsers()))



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
    test_suite.addTest(makeSuite(TestOwnershipByType))
    return test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
