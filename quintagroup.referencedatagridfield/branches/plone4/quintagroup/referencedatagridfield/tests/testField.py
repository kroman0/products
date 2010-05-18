import unittest
from types import ListType, TupleType, DictionaryType

from quintagroup.referencedatagridfield.tests.base import TestCase
from quintagroup.referencedatagridfield import ReferenceDataGridWidget


class TestField(TestCase):
    """ Field unit tests """

    def afterSetUp(self):
        self.createDemo()
        self.loginAsPortalOwner()
        self.refcat = self.portal.reference_catalog
        self.field = self.demo.getField('demo_rdgf')
        self.data = [{"uid": self.doc.UID(),
                      "link": "http://test.link",
                      "title": "test"},]

    def testColumnProperties(self):
        self.assertEqual(hasattr(self.field, "columns"), True)
        for column in ['title', 'link', 'uid']:
            self.assertEqual(column in self.field.columns, True)

    def testWidget(self):
        self.assertEqual(type(self.field.widget), ReferenceDataGridWidget)

    def testGetInitial(self):
        # If no data set - emty list must be returned
        field_data = self.field.get(self.demo)
        self.assertEqual(type(field_data), ListType)
        self.assertEqual(len(field_data), 0)

    def testGet(self):
        # if data set:
        # result is list with dictionary items, as in DataGridField
        self.field.set(self.demo, self.data)

        field_data = self.field.get(self.demo)
        self.assertEqual(type(field_data), ListType)
        self.assertEqual(len(field_data), 1)

        # items in list is Dictionary
        item_data = field_data[0]
        self.assertEqual(type(item_data), DictionaryType)
        # Dictionary contains uid, link, title keys
        self.assertEqual(item_data.has_key("uid"), True)
        self.assertEqual(item_data.has_key("link"), True)
        self.assertEqual(item_data.has_key("title"), True)


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(TestDataGridRelatedField),
        ])
