#
# Tests for quintagroup.plonegooglesitemaps upgrading
#

from base import *
from Products.CMFPlone.utils import _createObjectByType
from Products.GenericSetup.upgrade import _upgrade_registry
from quintagroup.canonicalpath.interfaces import ICanonicalPath
from quintagroup.canonicalpath.interfaces import ICanonicalLink

class TestUpgrade(TestCase):

    def afterSetUp(self):
        self.setup = self.portal.portal_setup
        self.profile = "quintagroup.plonegooglesitemaps:default"

    def getUpgradeStep(self, sortkey):
        upgrades = self.setup.listUpgrades(self.profile, show_old=True)
        upgrade_id = upgrades[sortkey-1]["id"]
        step = _upgrade_registry.getUpgradeStep(self.profile, upgrade_id)
        return step

    def test_upgradeStepsRegistration(self):
        # Test upgrade steps
        upgrades = self.setup.listUpgrades(self.profile, show_old=True)
        self.assertEqual(len(upgrades), 2)
        self.assertEqual(upgrades[0]["title"].endswith("1.0 to 1.1"), True)
        self.assertEqual(upgrades[1]["title"].endswith("1.1 to 1.2"), True)

    def test_upgradeSetupRegistration(self):
        # Test registered upgrade profiles
        pids = [i['id'] for i in self.setup.listProfileInfo()]
        self.assertEqual("quintagroup.plonegooglesitemaps:upgrade_1_0_to_1_1" in pids, True)
        self.assertEqual("quintagroup.plonegooglesitemaps:upgrade_1_1_to_1_2" in pids, True)

    def test_step_1_0_to_1_1(self):
        # Prepare testing data
        catalog = self.portal.portal_catalog
        if "canonical_path" in catalog._catalog.names:
            catalog.delColumn("canonical_path")
        # Upgrade to 1.1 version
        step = self.getUpgradeStep(1)
        if step is not None:
            step.doStep(self.setup)
        # canonical_path column must be added to portal_catalog
        self.assertEqual("canonical_path" in catalog._catalog.names, True)

    def test_step_1_1_to_1_2(self):
        # Prepare testing data
        catalog = self.portal.portal_catalog
        doc = _createObjectByType('Document', self.portal, id='test_doc')
        ICanonicalPath(doc).canonical_path = "/my_test_doc"
        if not "canonical_path" in catalog._catalog.names:
            catalog.addColumn("canonical_path")
        # Upgrade to 1.2 versionb
        step = self.getUpgradeStep(2)
        if step is not None:
            step.doStep(self.setup)
        # canonical_link column replace canonical_path one in the portal_catalog
        self.assertEqual("canonical_link" in catalog._catalog.names, True)
        self.assertEqual("canonical_path" in catalog._catalog.names, False)
        # canonical_link property refactored from canonical_path one for the object
        migrated_link = self.portal.absolute_url() + '/my_test_doc'
        self.assertNotEqual(ICanonicalPath(doc).canonical_path, "/my_test_doc")
        self.assertEqual(ICanonicalLink(doc).canonical_link, migrated_link)
        # canonical_link brain must contains updated canonical_link data
        brain = catalog(id="test_doc")[0]
        self.assertEqual(brain.canonical_link, migrated_link)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUpgrade))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
#    framework()
