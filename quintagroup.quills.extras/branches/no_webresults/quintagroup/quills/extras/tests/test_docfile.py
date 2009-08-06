# -*- coding: utf-8 -*-
from base import *
from Products.QuillsEnabled.tests import test_docfile

for x in ZOPE_DEPS + PLONE_DEPS:
    ztc.installProduct(x)

ptc.setupPloneSite(products=PLONE_DEPS)

test_suite = test_docfile.test_suite
