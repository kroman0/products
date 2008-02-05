import string
from StringIO import StringIO
from zLOG import LOG, INFO
from Products.CMFCore.utils import getToolByName
from Products.%(SKIN_PRODUCT_NAME)s.config import *
from Products.%(SKIN_PRODUCT_NAME)s.Extensions.utils import *

CHECKED_MESSAGE = "The base installation checkings completed."

def prepareInstallation(portal, pp, product, out):
    checkSuccessInstall(product)
    uninstallOtherSkinProducts(portal)
    if not ('uninstall_properties' in pp.objectIds()) :
        pp.addPropertySheet(id='uninstall_properties', title= 'uninstall_properties')
        print >> out, "Created 'portal_properties.uninstall_properties' PropertySheet (UP) for backup purpose"

def checkSuccessInstall(product):
    # Check for successfully completed 1 installation step
    transcript = getattr(product,'transcript',None)
    if transcript:
        msg = str(transcript[0]['msg'])
        if msg.find(CHECKED_MESSAGE) < 0 :
            product.log("First part installation procedure not completed - installation terminated.")
            raise

def uninstallOtherSkinProducts(portal):
    qi=getToolByName(portal, 'portal_quickinstaller', None)
    if not qi:
        raise Exception("Can't work without QuickInstaller tool.")
    # Get installed products
    installed_products = [getattr(qi, p_dict['id']) \
                          for p_dict in qi.listInstalledProducts()
                          if p_dict['id'] != PRODUCT_NAME]
    seek_str = "%%s generated product" %% GENERATOR_PRODUCT
    installed_skin_products = []
    # Looking for installed skin-products
    for p in installed_products:
        transcript = p.getTranscriptAsText()
        if transcript.find(seek_str) >= 0 :
            installed_skin_products.append(p.getId())
    # Uninstall found skin-products
    if installed_skin_products:
        qi.uninstallProducts(products=installed_skin_products)

def install(self):
    # Checking base condition for installation
    skinsTool = getToolByName(self, 'portal_skins')
    # Checking for BASE_SKIN_NAME presenting in portal
    skin_names = skinsTool.getSkinSelections()
    if not BASE_SKIN_NAME in skin_names:
        raise AttributeError("Impossible installation without %%s skin." %% BASE_SKIN_NAME)
    # Checking for presenting lower_SKIN_NAME directory in portal skins
    lower_SKIN_NAME = string.lower(SKIN_NAME)
    if lower_SKIN_NAME in skinsTool.objectIds():
        raise AttributeError("%%s skin layer already exist in portal skins. Installation Impossible." %% lower_SKIN_NAME)
    return CHECKED_MESSAGE

# For prevent quickInstaller's intervention in uninstall process - use afterInstall
def afterInstall(self,product,reinstall):
    out=StringIO()
    # get all needed tools and some portal's core objects
    portal = getToolByName(self, 'portal_url').getPortalObject()
    pp = getToolByName(portal, 'portal_properties')
    portal_css = getToolByName(portal, 'portal_css', None)
    portal_js = getToolByName(portal, 'portal_javascripts', None)
    # Make main prepare procedures
    prepareInstallation(portal, pp, product, out)
    pp_up = pp.uninstall_properties
    # Install skin
    installSkin(portal, pp_up, out)
    # Register css resources
    if portal_css and DOES_COSTOMIZE_CSS:
        registerResource(pp_up, portal_css, portal_css.registerStylesheet, out \
                        ,CSS_LIST, SKIN_CSS_REGDATA, 'q_registered_css', CSS_REG_PROPS)
        print >> out, "Completed tuning CSS registry for new skin needs."
    # Register js resources
    if portal_js and DOES_COSTOMIZE_JS:
        registerResource(pp_up, portal_js, portal_js.registerScript, out \
                        ,JS_LIST, SKIN_JS_REGDATA, 'q_registered_js', JS_REG_PROPS)#---installJS---
        print >> out, "Completed tuning JS registry for new skin needs."
    # Customize slots    
    if LEFT_SLOTS or RIGHT_SLOTS:
        customizeSlots(portal, pp_up, out)
    # Import object(s) to portal
    if checkIfImport():
        res_import = performImportToPortal(portal)
        print >> out, res_import
    # FINAL customization call additional functions from config 
    if FINAL_CUSTOMIZATION_FUNCTIONS:
        dummy = [func(portal, out) for func in FINAL_CUSTOMIZATION_FUNCTIONS]
    print >> out, "%%s generated product." %% GENERATOR_PRODUCT
    print >> out, '=== Installation successfully completed. ==='
    product.log(out.getvalue())
    product._p_changed = 1 #XXX:NEED for stable writing 'out' log to qi on afterinstallation.
    return out.getvalue()

def uninstall(self):
    # get all needed tools and some portal's core objects
    portal = self.portal_url.getPortalObject()
    skinsTool = getToolByName(portal, 'portal_skins')
    pp = getToolByName(portal, 'portal_properties')
    portal_css = getToolByName(portal, 'portal_css', None)
    portal_js = getToolByName(portal, 'portal_javascripts', None)
    # Get all properies, saving during installation, for uninstalling
    actual_skin_name = getProperty(pp, 'uninstall_properties', 'q_actual_skin_name',default=SKIN_NAME)
    initial_skin = getProperty(pp, 'uninstall_properties', 'q_default_skin',default="")
    original_css_list = getProperty(pp, 'uninstall_properties', 'q_registered_css')
    original_js_list = getProperty(pp, 'uninstall_properties', 'q_registered_js')
    orig_left_slots = getProperty(pp, 'uninstall_properties','q_left_slots')
    orig_right_slots = getProperty(pp, 'uninstall_properties','q_right_slots')
    # Remove 'uninstall_properties' from portal_properties
    if 'uninstall_properties' in pp.objectIds() :
        pp.manage_delObjects(ids=['uninstall_properties',])
    # Uninstall skin
    uninstallSkin(skinsTool, actual_skin_name, initial_skin)
    # Unregister skin's CSS-es from portal_css. Only for Plone 2.1+
    if portal_css and DOES_COSTOMIZE_CSS:
        uninstallResource(portal_css, original_css_list, CSS_LIST, portal_css.registerStylesheet)
    # Unregister skin's JS-s from portal_javascripts. Only for Plone 2.1+
    if portal_js and DOES_COSTOMIZE_JS:
        uninstallResource(portal_js, original_js_list, JS_LIST, portal_js.registerScript)
    # Return site's column slots list unless Skin product installation
    if orig_left_slots:
        portal.left_slots = tuple(orig_left_slots)
    if orig_right_slots:
        portal.right_slots = tuple(orig_right_slots)
