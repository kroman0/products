Introduction
============

Overview
--------
A product for switching themes by domain.

Installation
------------
Using portal_setup/quickinstaller - install product

Than in portal_properties/skin_switcher properties sheet
set following properties:

  - domain prefix for skin switching in 'theme_switch_prefix' property.
  - theme name for switching to if domain starts with specified prefix

If in config module 'USE_FS_CONFIG' set to `True` - than installation
not needed. This case usefull for zope instance with single plone
instance.
