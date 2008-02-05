## Script (Python) "qpt_delete"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= idx, id
##title=
##

act_tool = context.portal_actions
actions = act_tool.listActionInfos([],context,0,0,0)
tabs = filter(lambda a: a['category'] == 'portal_tabs', actions)
if tabs[int(idx)]['id'] == id:
    act_tool.deleteActions([actions.index(tabs[int(idx)]),])
