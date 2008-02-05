## Controller Python Script "ping_now"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=
##
status, message = context.portal_pingtool.pingFeedReader(context)
return state.set(status=status, portal_status_message=message)
