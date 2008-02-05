## Controller Script Python "validate_config"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state  
##bind subpath=traverse_subpath
##parameters=
##title=validates the email adresses

from Products.CMFCore.utils import getToolByName

form = context.REQUEST.form
email_key = 'Email_of_discussion_manager'

if email_key in form:
    email = form[email_key] 
    pu = getToolByName(context, 'plone_utils')
    if not pu.validateEmailAddresses(email):
        state.setError(email_key, 'Please submit a valid e-mail address.')

if state.getErrors():
    return state.set(status='failure', portal_status_message='Please correct the indicated errors.')
else:
    return state

