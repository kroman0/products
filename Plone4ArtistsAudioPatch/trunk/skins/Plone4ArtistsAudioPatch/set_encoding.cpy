# Controller Python Script "set_encoding"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=
#

encoding = context.REQUEST.get('encoding')

context.restrictedTraverse('@@audio_encoded').setEncoding(encoding)

return state.set(portal_status_message="Audio tag's text encoding setted to '%s'" % encoding)