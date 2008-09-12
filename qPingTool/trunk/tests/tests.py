import unittest
from zope.testing import doctestunit
from Testing.ZopeTestCase import FunctionalDocFileSuite as FileSuite

from zope.app.tests.placelesssetup import setUp, tearDown
from Products.PloneTestCase import PloneTestCase as PloneTestCase

class FunctionalTestCase(PloneTestCase.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """

    def afterSetUp(self):
        super(FunctionalTestCase, self).afterSetUp()

        self.uf = self.portal.acl_users
        self.uf.userFolderAddUser('root', 'secret', ['Manager'], [])

    def loginAsManager(self, user='root', pwd='secret'):
        """points the browser to the login screen and logs in as user root with Manager role."""
        self.basic_auth = '%s:%s' % (user, pwd)
        self.login('root')


def test_suite():
    return unittest.TestSuite([
        
        doctestunit.DocTestSuite(
            module='Products.qPingTool.adapter',
            setUp=setUp, tearDown=tearDown),
        
        FileSuite(
            'browser.txt', package='Products.qPingTool.tests',
            test_class=FunctionalTestCase,),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
