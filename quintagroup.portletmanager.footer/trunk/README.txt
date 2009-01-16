Introduction
============

This package adds portlet manager in the page footer.

Installation
============

If you are using buildout:
    
    * copy package to ``src`` directory
    * add it in ``buildout.cfg``
    * start zope and install it with QuickInstaller

If you manually created zope instance:

    * cd quintagroup.portletmanager.footer
    * copy ``quintagroup`` directory and all it's contents to ``lib/python`` 
      directory
    * copy file ``quintagroup.portletmanager.footer-configure.zcml``
      to ``etc/package-includes`` directory
    * start zope and install it with QuickInstaller

Uninstallation
==============

    * uninstall package in QuickInstaller and stop zope
    * remove package from ``buildout.cfg`` or zcml slug that was copied
      to ``etc/package-includes``
    * remove package from directory where it was copied to (if you don't
      need to use it in the future).
