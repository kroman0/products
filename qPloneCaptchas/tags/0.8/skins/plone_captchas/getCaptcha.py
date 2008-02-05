## Script (Python) "getCaptcha"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
from DateTime import DateTime
from Products.qPloneCaptchas.utils import encrypt
purl = context.portal_url()
date = str(DateTime().timeTime())
key = encrypt('pAss'+date)
return {'key':key, 'evalkey':date}
