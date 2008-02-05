## Controller Script Python "validate_talkback"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=subject='',body_text='',require_email, email=''
##title=validates a discussion entry
##
from Products.CMFCore.utils import getToolByName

dtool = context.portal_discussion
try:
    content = context.parentsInThread()[0]
except AttributeError:
    content = context
if not dtool.isDiscussionAllowedFor(content):
    raise Exception, "Discussion not allowed."

if not subject:
    state.setError('subject', context.translate('Please submit a subject.', domain="plonecomments"), 'subject_required')

if not body_text:
    state.setError('body_text', context.translate('Please submit a body.', domain="plonecomments"), 'body_required')
    
if require_email != 'False':
    if not (email and context.portal_registration.isValidEmail(email)):
        state.setError('email', context.translate('Please submit email.', domain="plonecomments"), 'email_required')

if hasattr(context, 'captcha_validator'):
    context.captcha_validator()

pp = getToolByName(context, 'portal_properties')
isForAnonymous = pp['qPloneComments'].getProperty('enable_anonymous_commenting', None)
if isForAnonymous:
    pm = getToolByName(context, 'portal_membership')
    isAnonym = pm.isAnonymousUser()
    if isAnonym:
        req = context.REQUEST
        if not (req.form.has_key('Creator') and not req.form['Creator'] == ""):
            state.setError('Creator', context.translate('Please enter your name.', domain="plonecomments"), 'name_required')

if state.getErrors():
    return state.set(status='failure', portal_status_message='Please correct the indicated errors.')
else:
    return state
