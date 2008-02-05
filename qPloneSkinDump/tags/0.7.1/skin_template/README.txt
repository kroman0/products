%(SKIN_PRODUCT_NAME)s

Installation

You can install this skin in the same way as any other Plone product:

  1. Install as Zope product: extract Plone skin from archive to directory of products and restart Zope (Plone).

  2. If you have access to file system - Set/Check in product's config.py constants.

  3. Install in your Plone instance with QuickInstaller 'Plone Control Panel' -> 'Add/remove Products'

  4. Now your Plone site should have the corresponding skin look.

Note: 

1. SkinName was created with "Plone skin dump product":http://quintagroup.com/services/plone-development/products/skin-dump
2. When you install this skin in Plone Control Panel
3. all other skins created with "Plone skin dump":http://quintagroup.com/services/plone-development/products/skin-dump will be automatically uninstalled.
4. Chosed in config.py import polisy (by constant IMPORT_POLICY from list ["only_new","backup","overwrite"])
   define the import procedure behavior when the same id meeted in portal root. On uninstall back_[date] directory
   and added during installation objects not removed - this behavior choosed for more safety.

Other skins created with  "Plone skin dump":http://quintagroup.com/services/plone-development/products/skin-dump can be found at
"Quintagroup Alternative Plone Skins project":http://skins.quintagroup.com/
