## Controller Python Script "getSiloData"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Update Folder Property
##parameters=
#

prop_dict = context.getSiloNavigationDictionary()

if not prop_dict:
    return []

if context.portal_type in ['Folder', 'Large Plone Folder', 'CMFFolder']: CONTEXT = context
else: CONTEXT = context.aq_parent

return [prop_dict[item] for item in CONTEXT.objectIds() if item in prop_dict.keys()]