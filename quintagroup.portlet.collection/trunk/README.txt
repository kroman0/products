Introduction
============

This package extends collection portlet with some useful features:
 - configurable appearance of portlet item . You can specify what
   attributes to display in portlet. By default 'Title' and
   'Description' attributes are configurable.

 - configurable portlet style. You can set particular style for particular
   portlet. To define your own styles for portlets, you should edit special
   property named 'portlet_dropdown'. This property is located in
   'portal_properties-> qcollectionportlet_properties'. To create
   new style - add new line containing two values divided by pipe. The first
   value is a css style class that will be added to portlet, the second value
   is a label that will be shown in portlet dropdown menu.
   For example: portletStaticClassOne|Class One

 - more... link for each portlet item . You can enable showing  more link
   for every item  displayed in portlet.

 - configurable linking for portlet items. There is boolean field
   named 'Link title', if enabled - item's title will be linked to the
   corresponding object.

 - batching. Portlet items can be split into pages. You can specify number
   of items to be displayed on page.
