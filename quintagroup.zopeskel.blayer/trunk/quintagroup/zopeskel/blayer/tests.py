# -*- coding: utf-8 -*-

from zopeskel.tests.test_zopeskeldocs import *

def test_suite():
    flags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE |
             doctest.REPORT_ONLY_FIRST_FAILURE)

    curr_dir = os.path.abspath(os.path.dirname(__file__))
    if curr_dir not in sys.path:
        sys.path.append(curr_dir)

    suite = unittest.TestSuite([
        doctest.DocFileSuite(
            'README.txt', package='quintagroup.zopeskel.blayer',
            setUp=testSetUp, tearDown=testTearDown,
            optionflags=flags, globs=globals()),

        ])
    suite.layer = ZopeSkelLayer
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
