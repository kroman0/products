Introduction
============

quintagroup.portlet.cumulus is a Plone product that allows you to add tag cloud
portlets to your Plone site. Your site's tags (content categories are used as 
tags) are displayed using a Flash movie that rotates them in 3D. It works just 
like a regular tags cloud, but is more visually exciting. This is the WordPress 
WP-Cumulus plugin ported to Plone as a portlet.

When you add this portlet anywhere in the site it will display all site's tags. 
If you have installed QullsEnabled product this portlet will display only blog's 
tags when rendered inside blog.

Usage
-----

* Install "Tag cloud (cumulus) portlet" with QuickInstaller.

* Select Tag Cloud (cumulus) portlet from Add portlet drop-down menu.

* Provide your own values for portlet configuration if needed.

* Save changes.

Supported Plone version
-----------------------

* 3.x

FAQ
---

From what version of WP-Cumulus WordPress plugin this product was ported?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's ported from WP-Cumulus 1.20.

Some characters are not showing up
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Because of the way Flash handles text, only Latin characters are supported in 
the current version. This is due to a limitation where in order to be able to 
animate text fields smoothly the glyphs need to be embedded in the movie. The 
Flash movie's source code is available for download through Subversion. Doing so 
will allow you to create a version for your language. There's a text field in 
the root of the movie that you can use to embed more characters. If you change 
to another font, you'll need to edit the Tag class as well.

Where can I find more information?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

WP-Cumulus WordPress plugin homepage: http://wordpress.org/extend/plugins/wp-cumulus/.

Author
------

* Bohdan Koval

Copyright (c) "Quintagroup": http://quintagroup.com/, 2009.

support@quintagroup.com * quintessence of modern business
