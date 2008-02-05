## Controlled Python Script "validate_mapkeys"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters= map_api_keys=''
##title=
##

if not map_api_keys:
    state.setError('map_api_keys', 'This field is required, please provide some information.')

if map_api_keys:
    for row in map_api_keys:
        i = map_api_keys.index(row) + 1
        if row == '':
            state.setError('map_api_keys', 'Line %d is empty.' % i)
            break
        if row.find('|') == -1:
            state.setError('map_api_keys', 'In line %d skipped pipe (|) symbol.' % i)
            break
        elif row.find('|') == 0:
            state.setError('map_api_keys', 'In line %d skipped portal root before pipe (|) symbol.' % i)
            break
        elif row.find('|') == len(row)-1:
            state.setError('map_api_keys', 'In line %d skipped map api key after pipe (|) symbol.' % i)
            break

if state.getErrors():
    return state.set(status='failure', portal_status_message='Please correct the indicated errors.')
else:
    return state

