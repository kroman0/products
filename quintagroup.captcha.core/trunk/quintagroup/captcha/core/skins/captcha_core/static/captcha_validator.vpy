from Products.CMFCore.utils import getToolByName

from quintagroup.captcha.core import ProductMessageFactory as _
from quintagroup.captcha.core.utils import decrypt, parseKey, \
    encrypt1, getWord
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

img = getattr(context, '%s.jpg' % index)
solution = img.title
enc = encrypt1(test_key)
captcha_tool = getToolByName(context, 'portal_captchas')
#import pdb;pdb.set_trace()
if (enc != solution) or (captcha_tool.has_key(decrypted_key)) \
    or (DateTime().timeTime() - float(date)>3600):
    #message = _(u"Please re-enter validation code.")

    # message = _(u"Please re-enter validation code.: %s, %s, %s, %s" % tuple(map(str, [enc, solution,captcha_tool.has_key(decrypted_key), DateTime().timeTime() - float(date)>3600] )))
    message = _(u"Please re-enter validation code.: hashkey='%s', test_key='%s', captcha_key='%s', decrypted_key='%s'; %s, %s" % tuple(map(str, [hashkey, test_key, context.captcha_key, decrypted_key, index, test_key] )))

    context.plone_utils.addPortalMessage(message, 'error')
    state.setError('key', message, 'key_required')
    return state.set(status="failure")
else:
    captcha_tool.addExpiredKey(decrypted_key)
    return state.set(status="success")
