Introduction
============

This package allows Plone websites display multilevel portal dropdown menu based
on portal actions settings and site structure.


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

