# -*- coding: utf-8 -*-
# Standard library imports
import unittest
from base import *
from Products.QuillsEnabled.tests import test_doctests

test_suite = test_doctests.test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')