import unittest

from zope.publisher.browser import TestRequest
from zope.formlib.namedtemplate import INamedTemplate
from zope.component import queryAdapter, queryMultiAdapter

from Products.Five import BrowserView

from quintagroup.referencedatagridfield import ReferenceDataGridWidget
from quintagroup.referencedatagridfield.tests.base import TestCase


class TestPopupRegistrations(TestCase):
    """Test popup related adapters registration."""

    def afterSetUp(self):
        self.req = TestRequest()

    def test_CustomNamedTemplate(self):
        view = BrowserView(self.portal, self.req)
        custom_named_template = queryAdapter(view, INamedTemplate, name="datagridref_popup")
        self.assertNotEqual(custom_named_template, None)
        
    def test_RefDataGridBrowser_popup(self):
        popup_page = queryMultiAdapter((object(), self.req), name="refdatagridbrowser_popup")
        self.assertNotEqual(popup_page, None)

    def test_WidgetBindToNamedTemplate(self):
        rdgw_props = ReferenceDataGridWidget._properties
        self.assertEqual(rdgw_props.get("popup_name", ""), "datagridref_popup")


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(TestPopupRegistrations),
        ])
