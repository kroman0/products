from Products.qPloneCaptchas.utils import decrypt, parseKey, \
     encrypt1, getWord
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
try:
    from Products.CMFPlone import MessageFactory
    _ = MessageFactory('qplonecaptchas')
except ImportError:
    from Products.PlacelessTranslationService.MessageID import MassageIDFactory
    _ = MessageIDFactory('qplonecaptchas')

if state.getStatus()=='failure':
    return  state
request = context.REQUEST

test_key = request.get('key', '')
hashkey = request.get('hashkey', '')
decrypted_key = decrypt(context.captcha_key, hashkey)
parsed_key = parseKey(decrypted_key)

index = parsed_key['key']
date = parsed_key['date']

enc = test_key
solution = getWord(int(index))
captcha_tool = getToolByName(context, 'portal_captchas')
if (enc != solution) or (captcha_tool.has_key(decrypted_key)) \
    or (DateTime().timeTime() - float(date)>3600):
    state.setError('key', _("Please re-enter validation code."), 'key_required')
    return state.set(status="failure", portal_status_message = _("Please re-enter validation code."))
else:
    captcha_tool.addExpiredKey(decrypted_key)
    return state.set(status="success")
