## Controller Script Python "validate_talkback"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=subject='',body_text=''
##title=validates a discussion entry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

dtool = context.portal_discussion
try:
    content = context.parentsInThread()[0]
except AttributeError:
    content = context
if not dtool.isDiscussionAllowedFor(content):
    raise Exception, "Discussion not allowed."

if not subject:
    state.setError('subject', _(u'Please submit a subject.'), 'subject_required')

if not body_text:
    state.setError('body_text', 'Please submit a body.', 'body_required')

pp = getToolByName(context, 'portal_properties')
isForAnonymous = pp['qPloneComments'].getProperty('enable_anonymous_commenting', None)
if isForAnonymous:
    pm = getToolByName(context, 'portal_membership')
    isAnonym = pm.isAnonymousUser()
    if isAnonym:
        req = context.REQUEST
        if not (req.form.has_key('Creator') and not req.form['Creator'] == ""):
            state.setError('Creator', 'Please enter your name.', 'name_required')

if state.getErrors():
    context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'))
    return state.set(status='failure')
else:
    return state
