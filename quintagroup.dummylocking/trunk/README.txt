quintagroup.dummylocking
========================

Overview
--------

  This is a package that turns off Plone locking right after installation. It overrides standard locking adapter with the one that does nothing.
 
  Plone locking mechnism prevents concurrent through-the-web editing in Plone, but sometimes excessive locking can interfere with normal Plone workflow. 

Requirements
------------

* Plone 3.x

In Plone 3.3 you can disable through-the-web locking in Plone Control Panel and
this package isn't needed.

Author
------

* Bohdan Koval
