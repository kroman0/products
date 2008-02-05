## Controller Script (Python) "prefs_captchas_setup"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Set necessary skin
##
from Products.CMFCore.utils import getToolByName
import string
def exchangeLayers(layer1, layer2):
    skinstool = getToolByName(context, 'portal_skins')
    for skin in skinstool.getSkinSelections():
        path = skinstool.getSkinPath(skin)
        path = map( string.strip, string.split( path,',' ))
        try:
            i = path.index(layer1)
            path.remove(layer1)
            path.insert(i, layer2)
        except ValueError:
            pass
        path = string.join( path, ', ' )
        skinstool.addSkinSelection( skin, path )

form = context.REQUEST.form
ct = form['static_captchas']

if ct == 'static':
    exchangeLayers('plone_captchas/dynamic', 'plone_captchas/static')
    layer = 'static'
else:
    exchangeLayers('plone_captchas/static', 'plone_captchas/dynamic')
    layer = 'dynamic'

return state.set(portal_status_message = 'Captchas changed to %s'%layer)