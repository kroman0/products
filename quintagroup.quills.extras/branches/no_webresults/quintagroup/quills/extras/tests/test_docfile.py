# -*- coding: utf-8 -*-
import unittest
from base import *
from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite
from Products.PloneTestCase.layer import PloneSite
from Products.QuillsEnabled.tests import test_docfile

for x in ZOPE_DEPS + PLONE_DEPS:
    ztc.installProduct(x)

ptc.setupPloneSite(products=PLONE_DEPS)

#test_suite = test_docfile.test_suite

def test_suite():
    suite = unittest.TestSuite(())

    suite.addTest(ZopeDocFileSuite(
        'workflowstates.txt',
        package='quills.app.tests',
        test_class=test_docfile.QuillsDocTestCase,
        optionflags=test_docfile.optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'tests.txt',
        package='quills.core.tests',
        test_class=test_docfile.QuillsDocTestCase,
        optionflags=test_docfile.optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'tests.txt',
        package='quills.core.tests',
        test_class=test_docfile.QuillsContributorDocTestCase,
        optionflags=test_docfile.optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'tests.txt',
        package='quills.core.tests',
        test_class=test_docfile.QuillsDocTestCase,
        optionflags=test_docfile.optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'extras_browser.rst',
        package='quintagroup.quills.extras.tests',
        test_class=test_docfile.QuillsFunctionalTestCase,
        optionflags=test_docfile.optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'extras_browser.rst',
        package='quintagroup.quills.extras.tests',
        test_class=test_docfile.QuillsFunctionalTestCase,
        optionflags=test_docfile.optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'openBugs.rst',
        package='Products.QuillsEnabled.tests',
        test_class=test_docfile.QuillsFunctionalTestCase,
        optionflags=test_docfile.optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'fixedBugs.rst',
        package='Products.QuillsEnabled.tests',
        test_class=test_docfile.QuillsFunctionalTestCase,
        optionflags=test_docfile.optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'extras_fixedBugs.rst',
        package='quintagroup.quills.extras.tests',
        test_class=test_docfile.QuillsFunctionalTestCase,
        optionflags=test_docfile.optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'openBugs.rst',
        package='quills.app.tests',
        test_class=test_docfile.QuillsFunctionalTestCase,
        optionflags=test_docfile.optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'issue193.txt',
        package='quills.app.tests',
        test_class=test_docfile.QuillsFunctionalTestCase,
        optionflags=test_docfile.optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'syndication.rst',
        package='quills.app.tests',
        test_class=test_docfile.QuillsFunctionalTestCase,
        optionflags=test_docfile.optionflags,
        )
    )

    suite.addTest(ZopeDocFileSuite(
        'tests.txt',
        package='quills.core.tests',
        test_class=test_docfile.QuillsContributorDocTestCase,
        optionflags=test_docfile.optionflags,
        )
    )

    suite.layer = PloneSite
    return suite
