##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=trbacks_checked
##title=
##
bl_counter, del_counter = context.portal_trackspam.blackListAndRemove(trbacks_checked)
return state.set(status = 'success', portal_status_message="%s trackbacks where deleted. %s new urls where added to black list." % (del_counter, bl_counter))