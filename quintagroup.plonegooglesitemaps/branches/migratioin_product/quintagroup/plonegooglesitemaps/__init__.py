import sys
from AccessControl import allow_module

allow_module('quintagroup.plonegooglesitemaps.utils.py')
allow_module('quintagroup.plonegooglesitemaps.config.py')

from zope.i18nmessageid import MessageFactory
from quintagroup.plonegooglesitemaps import config

from Products.Archetypes import atapi
from Products.CMFCore.utils import ContentInit
from Products.CMFCore.permissions import setDefaultRoles

# Define a message factory for when this product is internationalised.
# This will be imported with the special name "_" in most modules. Strings
# like _(u"message") will then be extracted by i18n tools for translation.

qPloneGoogleSitemapsMessageFactory = MessageFactory('qPloneGoogleSitemaps')

def initialize(context):
    """Initializer called when used as a Zope 2 product.

    This is referenced from configure.zcml. Regstrations as a "Zope 2 product"
    is necessary for GenericSetup profiles to work, for example.

    Here, we call the Archetypes machinery to register our content types
    with Zope and the CMF.
    """

    # Retrieve the content types that have been registered with Archetypes
    # This happens when the content type is imported and the registerType()
    # call in the content type's module is invoked. Actually, this happens
    # during ZCML processing, but we do it here again to be explicit. Of
    # course, even if we import the module several times, it is only run
    # once.

    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    # Now initialize all these content types. The initialization process takes
    # care of registering low-level Zope 2 factories, including the relevant
    # add-permission. These are listed in config.py. We use different
    # permissions for each content type to allow maximum flexibility of who
    # can add which content types, where. The roles are set up in rolemap.xml
    # in the GenericSetup profile.

    for atype, constructor in zip(content_types, constructors):
        ContentInit('%s: %s' % (config.PROJECTNAME, atype.portal_type),
            content_types      = (atype,),
            permission         = config.ADD_PERMISSIONS[atype.portal_type],
            extra_constructors = (constructor,),
            ).initialize(context)

    #
    # BBB: Create qPloneGoogleSitemaps module alias
    from quintagroup import plonegooglesitemaps
    from quintagroup.plonegooglesitemaps import interfaces
    from quintagroup.plonegooglesitemaps.content import sitemap
    # from quintagroup.plonegooglesitemaps import Extensions
    # from quintagroup.plonegooglesitemaps.Extensions import Install
    for k,v in (
            ('Products.qPloneGoogleSitemaps', plonegooglesitemaps),
            ('Products.qPloneGoogleSitemaps.config', config),
            ('Products.qPloneGoogleSitemaps.interfaces', interfaces),
            ('Products.qPloneGoogleSitemaps.content.sitemap', sitemap),
            # ('Products.qPloneGoogleSitemaps.Extensions', Extensions),
            # ('Products.qPloneGoogleSitemaps.Extensions.Install', Install),
        ):
        if not sys.modules.has_key(k):
            sys.modules[k] = v

