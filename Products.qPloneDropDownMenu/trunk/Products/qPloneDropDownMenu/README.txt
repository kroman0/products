Quintagroup Plone Drop Down Menu

  The product allows Plone websites to update multilevel portal
  dropdown menu and edit it within Plone.

  "Product Homepage":http://quintagroup.com/services/plone-development/products/ |
  "Download":http://sourceforge.net/projects/quintagroup

  (c) "Quintagroup":http://quintagroup.com/ , 2008. 

  support@quintagroup.com * quintessence of modern business

Requires

  Plone 4

Install

  1. Install with Quick Installer. 

Usage

  You have a list of items of your top level menu, which you can edit in
  'drop down menu' configlet form. Now, to add submenu to the certain 
  menu item, you need to add unordered list inside of top level menu 
  item ('<li>...</li>') after its title ('<a></a>')::

   <ul><li>...</li>...<li>...</li></ul>

  To make your changes live click 'save' button.

  Sample menu with 2 submenus::
 
   <li id="portaltab-index_html" class="plain"><a href="http://example.com/" accesskey="t">Home</a></li>
   <li id="portaltab-Members" class="plain"><a href="http://example.com/Members" accesskey="t">Members</a>
       <ul>
           <li><a href="http://example.com/Members/jdoe">John Doe</a><li>
           <li><a href="http://example.com/Members/mmajor">Mary Major</a></li>
       </ul>
   </li>
   <li id="portaltab-news" class="plain"><a href="http://example.com/news" accesskey="t">News</a></li>
   <li id="portaltab-events" class="plain"><a href="http://example.com/events" accesskey="t">Events</a>
       <ul>
           <li><a href="http://example.com/events/previous">Past Events</a></li>
           <li><a href="http://example.com/calendar">Calendar</a></li>
       </ul>
   </li>

  In this example we added submenus to our 'Members', and 'Events' tabs.


  Customize the following elements in your's css files to
  changed the appearance of drop down menu:

    * #portal-globalnav - global navigation bar
    * #portal-globalnav .csshover li.plain a, #portal-globalnav li a - global navigation link
    * #portal-globalnav .csshover li.plain a:hover, #portal-globalnav li a:hover - global navigation link hover
    * #portal-globalnav .csshover li.plain ul, #portal-globalnav li ul - global navigation drop-down box
    * #portal-globalnav .csshover li.plain ul li a, #portal-globalnav li ul li a - global navigation drop-down link
    * #portal-globalnav .csshover li.plain ul li a:hover, #portal-globalnav li ul li a:hover - global navigation
      drop-down link hover


You can click  button on 'drop down menu' configlet form to reset menu.
This can be usefull in case  broken html of menu code. Generated code is based
on status of 'Automatically generate tabs' in your 'Navigation settings'
However you will lose your previous code of menu with all submenus 
after click on 'regenerate menu'.

If you want to 'regenerate menu' you should pay attention to status of
'Automatically generate tabs' in your 'Navigation settings'.

Authors

  * Vitaliy Podoba
