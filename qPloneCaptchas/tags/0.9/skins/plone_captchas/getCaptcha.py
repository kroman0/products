## Script (Python) "getCaptcha"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
from Products.qPloneCaptchas.utils import getCaptchasCount, formKey, \
     encrypt

from Products.qPloneCaptchas.config import havePIL
from random import randint
key = formKey(randint(0, getCaptchasCount(havePIL)))
encrypted_key = encrypt(context.captcha_key, key)

return encrypted_key
