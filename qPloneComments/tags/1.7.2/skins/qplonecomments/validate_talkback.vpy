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
from Products.qPloneComments.config import PROPERTY_SHEET

if not subject:
    state.setError('subject', 'Please submit a subject.', 'subject_required')

if not body_text:
    state.setError('body_text', 'Please submit a body.', 'body_required')

pp = getToolByName(context, 'portal_properties')
isForAnonymous = pp[PROPERTY_SHEET].getProperty('Enable_Anonymous_Commenting', None)
if isForAnonymous:
    pm = getToolByName(context, 'portal_membership')
    isAnonym = pm.isAnonymousUser()
    if isAnonym:
        req = context.REQUEST
        if not (req.form.has_key('Creator') and not req.form['Creator'] == ""):
            state.setError('Creator', 'Please submit a Name.', 'name_required')

if state.getErrors():
    return state.set(status='failure', portal_status_message='Please correct the indicated errors.')
else:
    return state
