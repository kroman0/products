from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase

DEPENDENCIES = ['Archetypes']
PRODUCT_DEPENDENCIES = ['MimetypesRegistry', 'PortalTransforms',
                        'basesyndication', 'fatsyndication']

# Install all (product-) dependencies, install them too
for dependency in PRODUCT_DEPENDENCIES + DEPENDENCIES:
    ZopeTestCase.installProduct(dependency)

PRODUCTS = list(DEPENDENCIES)

PloneTestCase.setupPloneSite(products=PRODUCTS)

from Products.Five import zcml
import p4a.common
import p4a.audio
import p4a.fileimage
import p4a.audiopatch

def testclass_builder(**kwargs):   
    class PloneIntegrationTestCase(PloneTestCase.PloneTestCase):
        """Base integration TestCase for p4a.audio."""
    
        def _setup(self):
            PloneTestCase.PloneTestCase._setup(self)
            zcml.load_config('configure.zcml', p4a.common)
            zcml.load_config('configure.zcml', p4a.audio)
            zcml.load_config('configure.zcml', p4a.fileimage)
	    zcml.load_config('configure.zcml', p4a.audiopatch)

    for key, value in kwargs.items():
        setattr(PloneIntegrationTestCase, key, value)
    return PloneIntegrationTestCase
