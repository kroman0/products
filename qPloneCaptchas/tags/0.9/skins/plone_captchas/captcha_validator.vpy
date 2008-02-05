from Products.qPloneCaptchas.config import havePIL
from Products.qPloneCaptchas.utils import decrypt, parseKey, \
     encrypt1, getWord, addExpiredKey
from DateTime import DateTime

if state.getStatus()=='failure':
    return  state
request = context.REQUEST

test_key = request.get('key', '')
hashkey = request.get('hashkey', '')
decrypted_key = decrypt(context.captcha_key, hashkey)
parsed_key = parseKey(decrypted_key)
 
index = parsed_key['key']
date = parsed_key['date']

if havePIL:
    enc = test_key
    solution = getWord(int(index))
else:
    img = getattr(context, '%s.jpg' % index)
    solution = img.title
    enc = encrypt1(test_key)

if (enc != solution) or (context.portal_captchas.has_key(decrypted_key)) \
   or (DateTime().timeTime() - float(date)>3600):
   state.setError('key', 'Please re-enter validation code.', 'key_required')
   return state.set(status="failure", portal_status_message = "Please re-enter validation code.")
else:
    addExpiredKey(context, decrypted_key)
    return state.set(status="success")
