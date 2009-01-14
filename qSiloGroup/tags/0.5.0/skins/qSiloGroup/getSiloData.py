## Controller Python Script "getSiloData"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Update Folder Property
##parameters=
#

from Products.qSiloGroup.utils import getCurrentFolder

prop_dict = context.getSiloNavigationDictionary()

if not prop_dict:
    return []

CONTEXT = getCurrentFolder(context)

return [prop_dict[item] for item in CONTEXT.objectIds() if item in prop_dict.keys()]