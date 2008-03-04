## Script (Python) "qpt_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= idx, num, visibility=[], category='portal_tabs'
##title=
##

req = context.REQUEST
params = {'self':context,'num':num, 'category':category}
fields = ['name', 'action', 'id', 'condition']
if visibility != []: params['visibility'] = visibility
for item in fields:
    params[item] = req.get('i'+idx+'_'+item, None)

from Products.qPloneTabs.utils import editAction
return editAction(**params)