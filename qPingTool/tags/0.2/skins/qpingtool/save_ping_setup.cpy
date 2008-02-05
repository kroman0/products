## Controller Python Script "createObject"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters= enable_ping=0,ping_sites=[],REQUEST=None
##title=
##
status, message = context.portal_pingtool.setupPing(context, enable_ping, ping_sites)
return state.set(status=status, portal_status_message=message)
    