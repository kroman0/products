## Controller Script Python "validate_reply"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state  
##bind subpath=traverse_subpath
##parameters=
##title=validates discussion_reply

if hasattr(context, 'review_state') and not context.review_state=="published":
    from Products.qPloneComments.utils import setStatusMsg
    msg = "Reply not allowed because the response is to a comment waiting to be " \
           "approved. Please wait for the comment to be approved before replying."

    state.set(status='failure', portal_status_message=msg)
    return state.set(status='failure')

    # Resolve needless redirection, which leed to loosing portal status message.
    #try:
        #redirect_target = context.plone_utils.getDiscussionThread(context)[0]
    #except:
        #redirect_target = context
    #setStatusMsg(state, context, msg)
    #return state.set(status='failure', context=redirect_target)

return state