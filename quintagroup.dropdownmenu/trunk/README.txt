Introduction
============

This package allows Plone websites display multilevel portal dropdown menu based
on portal actions settings and site structure.

You may ask why we may need one more dropdown menu product for Plone having
already qPloneDropDownMenu, webcouturier.dropdownmenu and much more products
providing similar functionality. While qPloneDropDownMenu product just displays
manually edited html code with nested unordered list webcouturier.dropdownmenu
went further and is trying to display submenus for each standard portal tab be
it action from portal_actions tool or be it auto generated tab based on content
structure.

But neither of those products use newly introduced portal_actions tool's
feature: nested categories. That's why quintagroup.dropdownmenu package was
introduced. It allows to build multilevel portal dropdown menu based on nested
portal_actions categories inside portal_tab category as well as on portal
content structure.

It also allows you to define if to put content tabs before or after action tabs,
and a bit more... For details see below.


Requires
--------

  Plone 3.0+


Install
-------

  * first follow instructions inside docs/INSTALL.txt document

  * then install product with Quick Installer


Migration from qPloneDropDownMenu
---------------------------------

In case qPloneDropDownMenu product was previously installed in a site
installation procedure will automatically detect legacy settings and migrate
it to a newly created tool along with removing old portal_dropdownmenu one.

Also installation procedure will uninstall qPloneDropDownMenu product itself
(in case it's still installed) and clean up everything after it.

Note: to successfully migrate old tabs it's required to have a valid html
markup, otherwise migration procedure won't be able to move tabs correctly.

