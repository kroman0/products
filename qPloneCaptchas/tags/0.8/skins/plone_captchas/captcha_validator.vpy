if state.getStatus()=='failure':
    return  state
request = context.REQUEST
key = request.get('hashkey', '')
evalkey = request.get('evalkey', '')
test_key = request.get('key', '')
if DateTime().timeTime() - float(evalkey)>3600:
   return  state.set(status="failure", portal_status_message="Please re enter key")

from Products.qPloneCaptchas.config import CAPTCHAS_COUNT
from Products.qPloneCaptchas.utils import encrypt
index = int(key[:4],16)%CAPTCHAS_COUNT
if index == 0:
    index = CAPTCHAS_COUNT
img = getattr(context, '%s.jpg' % index)
solution = img.title
enc = encrypt(test_key)

if enc != solution:
   state.setError('key', 'Please submit the validation code.', 'key_required')
   return  state.set(status="failure", portal_status_message="Please re enter validation code")
return  state.set(status="success")
