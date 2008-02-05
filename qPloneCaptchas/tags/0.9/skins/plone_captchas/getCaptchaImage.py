## Script (Python) "getCaptchaImage"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
from Products.qPloneCaptchas.utils import gen_captcha, decrypt, \
     getWord, parseKey
from Products.qPloneCaptchas.config import havePIL
hk = context.REQUEST.traverse_subpath[0]
dk = decrypt(context.captcha_key, hk)
key = parseKey(dk)['key']

if havePIL:
    im = gen_captcha(getWord(int(key)), 27)
    context.REQUEST.RESPONSE.setHeader('Content-Type', 'image/jpeg')
    context.REQUEST.RESPONSE.setHeader('Content-Length', im['size'])
    context.REQUEST.RESPONSE.setHeader('Accept-Ranges', 'bytes')
    return im['src']
else:
    img = getattr(context, '%s.jpg' % key)
    return img.index_html(context.REQUEST, context.REQUEST.RESPONSE)
