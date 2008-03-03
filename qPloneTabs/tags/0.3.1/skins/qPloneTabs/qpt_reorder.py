## Script (Python) "reorder"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= idxs=[], category='portal_tabs'
##title=
##

if not idxs: return 'No items'

from Products.qPloneTabs.utils import reorderActions

return reorderActions(context, idxs, category)