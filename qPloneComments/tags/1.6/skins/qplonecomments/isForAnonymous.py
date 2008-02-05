## Script (Python) "isForAnonymous"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.qPloneComments.utils import getProp

return getProp(context, "Enable_Anonymous_Commenting", False)
