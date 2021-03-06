Introduction
============

This package allows to build dropdown menu through the web with portal_actions.
Submenus are built from a tree of nested Category Actions and Actions.
The other strategy used to populate submenus is Plone default NavigationStrategy, 
the one used in navigation portlet.  

This project is successor of qPloneDropDownMenu. 

Building you dropdown menu with portal_actions
----------------------------------------------

Starting from Plone 3 portal actions introduced CMF Action Category 
containers, it opened opportunity to build nested actions trees. Though CMF Action 
Category does not behave as a regular action, it has different set of properties. 
We introduced convention in quintagroup.dropdownmenu that requires to have 
a specially named Action for each Actions Category. The id of each such action 
must be build using the rule: 
  
    action_id = prefix + category_id + suffix
   
where:
  
    'category_id' is id of correspondent CMF Action Category
    'prefix' defined in DropDownMenu configlet, default value ''
    'suffix' defined in DropDownMenu configlet, default value '_sub'

So, the actions structure can look like:

    / portal_tabs
    |- home
    |- blog_sub
    |-/ blog
    | |-- 2009
    | |-- 2010
     
By default the root of dropdown menu is 'portal_tabs' category.
 
Compatibility
-----------

  Plone 3.0 - 3.3
  Plone 4


Installation
------------

  * add quintagroup.dropdownmenu to your buildout
  * install in Plone with Quick Installer
  * find more details inside docs/INSTALL.txt 
