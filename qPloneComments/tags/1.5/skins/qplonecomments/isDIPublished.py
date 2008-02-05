## Script (Python) "isDIPublished"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

from Products.qPloneComments.utils import isPublished

return isPublished(context)