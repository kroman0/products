## Script (Python) "ifModerate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.qPloneComments.utils import getProp

return getProp(context, "Turning_on/off_Moderation", False)
