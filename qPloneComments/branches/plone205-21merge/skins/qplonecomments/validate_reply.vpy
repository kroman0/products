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
    return state.set(status='failure', portal_status_message="You can't add comment to not published reply.")

return state
