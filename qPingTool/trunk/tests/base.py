from Products.PloneTestCase import PloneTestCase as PloneTestCase

from Products.CMFCore.utils import getToolByName
from Products.qPingTool import PingTool
from Products.qPingTool.config import *

PRODUCTS = ['qPingTool', 'SimpleBlog']

map(PloneTestCase.installProduct, ('qPingTool', 'XMLRPCMethod', 'SimpleBlog'))

PloneTestCase.setupPloneSite(products=PRODUCTS)

class TestCase(PloneTestCase.PloneTestCase):
    """Base class used for test cases
    """
