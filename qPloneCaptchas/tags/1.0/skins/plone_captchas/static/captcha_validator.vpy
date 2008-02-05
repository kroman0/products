from Products.qPloneCaptchas.utils import decrypt, parseKey, \
     encrypt1, getWord #, addExpiredKey
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
if state.getStatus()=='failure':
    return  state
request = context.REQUEST

test_key = request.get('key', '')
hashkey = request.get('hashkey', '')
decrypted_key = decrypt(context.captcha_key, hashkey)
parsed_key = parseKey(decrypted_key)

index = parsed_key['key']
date = parsed_key['date']

img = getattr(context, '%s.jpg' % index)
solution = img.title
enc = encrypt1(test_key)
captcha_tool = getToolByName(context, 'portal_captchas')
if (enc != solution) or (captcha_tool.has_key(decrypted_key)) \
   or (DateTime().timeTime() - float(date)>3600):
   state.setError('key', 'Please re-enter validation code.', 'key_required')
   return state.set(status="failure", portal_status_message = "Please re-enter validation code.")
else:
    captcha_tool.addExpiredKey(decrypted_key)
    return state.set(status="success")
