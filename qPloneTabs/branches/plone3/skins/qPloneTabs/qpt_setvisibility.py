## Script (Python) "qpt_setvisibility"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= id, visibility
##title=
##

from Products.CMFCore.utils import getToolByName
obj = getToolByName(context, id, None)
if obj:
    if visibility == 'true': visibility = False
    else: visibility = True
    obj.update(excludeFromNav = visibility)

return "Visibility set to %s" % visibility