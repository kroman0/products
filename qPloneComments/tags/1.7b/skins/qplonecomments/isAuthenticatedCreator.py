## Script (Python) "isAuthenticatedCreator"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=creator
##title=
##

from Products.qPloneComments.utils import isAuthenticatedCreator

return isAuthenticatedCreator(context, creator)