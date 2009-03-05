## Controller Script Python "validate_setup"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state  
##bind subpath=traverse_subpath
##parameters=
##title=validates qpc setup
##
from Products.CMFCore.utils import getToolByName

form = context.REQUEST.form
email_key = 'email_discussion_manager'

if email_key in form:
    email = form[email_key] 
    pu = getToolByName(context, 'plone_utils')
    if not pu.validateEmailAddresses(email):
        from Products.qPloneComments.utils import getTranslFunction
        transl_func = getTranslFunction(context)
        state.setError(email_key, transl_func('Please submit a valid e-mail address.'))

if state.getErrors():
    return state.set(status='failure', portal_status_message='Please correct the indicated errors.')
else:
    return state

