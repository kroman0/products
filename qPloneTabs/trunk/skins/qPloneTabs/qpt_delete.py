## Script (Python) "qpt_delete"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= idx, id, category='portal_tabs'
##title=
##

from Products.qPloneTabs.utils import deleteAction

return deleteAction(context, idx, id, category)