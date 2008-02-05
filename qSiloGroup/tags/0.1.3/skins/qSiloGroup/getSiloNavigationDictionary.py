## Controller Python Script "getSiloNavigationDictionary"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Update Folder Property
##parameters=
#

if context.portal_type in ['Folder', 'Large Plone Folder', 'CMFFolder']: CONTEXT = context
else: CONTEXT = context.aq_parent

items = CONTEXT.getProperty('silo_items',None)

if not items:
    return {}

prop_dict = {}
for i in items:
    s = map(str, i.split('|'))
    try:
        if len(s) == 2:
            title = s[1]
            path = s[0]
        else:
            if s[1]: s[1] = '/'+s[1]
            title = s[2]
            path = s[0] + s[1]
        prop_dict[s[0]] = {'id': s[0], 'path':path, 'title':title}
    except: continue

return prop_dict