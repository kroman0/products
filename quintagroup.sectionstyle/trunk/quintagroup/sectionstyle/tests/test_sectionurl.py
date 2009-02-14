from quintagroup.sectionstyle.tests.base import TestCase


class TestSectionScript(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def test_getSectionFromURL(self):
        script = self.portal.getSectionFromURL
        self.assertEquals('', script())
        # now add property 'body_class' to portal
        self.portal.manage_addProperty('body_class', 'extraClass', 'string')
        self.assertEquals('extraClass', script())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSectionScript))
    return suite
