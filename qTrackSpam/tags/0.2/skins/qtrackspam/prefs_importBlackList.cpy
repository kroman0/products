##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=body,file
##title=
##

data=""
if file:
    file.seek(0)
    data = file.read()
context.portal_trackspam.setBlackList(body + data)
return state.set(status = 'success', portal_status_mesage='BLackList updated')
