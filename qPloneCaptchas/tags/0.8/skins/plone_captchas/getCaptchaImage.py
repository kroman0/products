## Script (Python) "getCaptchaImage"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
from Products.qPloneCaptchas.config import CAPTCHAS_COUNT
request = context.REQUEST
key = request.traverse_subpath[0]
index = int(key[:4],16)%CAPTCHAS_COUNT
if index == 0:
    index = CAPTCHAS_COUNT
img = getattr(context, '%s.jpg' % index)
return img.index_html(request, request.RESPONSE)
