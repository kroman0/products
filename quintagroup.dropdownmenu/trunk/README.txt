Introduction
============

This package allows Plone websites display multilevel portal dropdown menu based
on portal actions settings and site structure.

You may ask why we may need one more dropdown menu product for Plone, having
already qPloneDropDownMenu, webcouturier.dropdownmenu and other products
providing similar functionality. While qPloneDropDownMenu product just displays
manually edited html code with nested unordered list, webcouturier.dropdownmenu
went further and is trying to display submenus for each standard portal tab be
it action from portal_actions tool or be it auto generated tab based on content
structure.

But neither of those products use newly introduced portal_actions tool's
feature: nested categories. That's why quintagroup.dropdownmenu package was
introduced. It allows to build multilevel portal dropdown menu based on nested
portal_actions categories inside portal_tab category as well as based on portal
content structure.

It also allows you to define whether to put content tabs before or after action
tabs, and a bit more... For details see below.


Notes
-----

  * you may have actions/content-based tabs as deep as you wish, but then you'll
    need to tweek default dropdown menu css rules a bit, default css rules show
    only the first 4 levels of tabs

Requirement
-----------

  Plone 3.0+


Installation
------------

  * first follow instructions inside docs/INSTALL.txt document

  * then install product with Quick Installer in Plone


Migration from qPloneDropDownMenu
---------------------------------

In case qPloneDropDownMenu product was previously installed, it will
automatically detect legacy settings, migrate it to a newly created settings
registry and update portal_actions tool if required along with removing old
portal_dropdownmenu one.

Also installation procedure will uninstall qPloneDropDownMenu product itself
(in case it's still installed) and clean up everything after it.

Note: to successfully migrate old tabs it's required to have a valid html
markup, otherwise migration procedure won't be able to move tabs correctly.
