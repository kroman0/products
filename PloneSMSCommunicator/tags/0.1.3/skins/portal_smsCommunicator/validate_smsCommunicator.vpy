## Controller Python Script "validate_smsCommunicator"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters = server_url
##title=
##
from Products.PloneSMSCommunicator.Utils import isUrl
if isUrl(server_url):
    return state.set(status='success', portal_status_message='PloneSMSCommunicator properties was updated')
else:
    return state.set(status='failure', portal_status_message='Server address is incorrect')