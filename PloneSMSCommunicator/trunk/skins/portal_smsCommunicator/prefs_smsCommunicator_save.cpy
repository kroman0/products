##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=server_url, policy, mtMessageOriginator, provider_id, log_flag=None
##title=
##
request=context.REQUEST
props = {'server_url':server_url, 'policy':policy, 'mtMessageOriginator':mtMessageOriginator, 'provider_id':provider_id, 'log_flag':log_flag}
results = context.portal_smsCommunicator.setProperties(**props)
return state