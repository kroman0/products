## Script (Python) "gsm_edit_settings"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##bind state=state
##parameters=
##title=Configure Plone Google Sitemap
##

from Products.CMFCore.utils import getToolByName
from Products.qPloneGoogleSitemaps.utils import ping_google
#import Products.qPloneGoogleSitemaps.config as config

portal_url = getToolByName(context,'portal_url')
portalURL = portal_url()
portal = portal_url.getPortalObject()
req = context.REQUEST

if req.get('form.button.Add', False):
    return req.RESPONSE.redirect(
                "%s/createObject?type_name=Sitemap" % portalURL)
else:
    smtypes = req.get('smtypes', [])

    message = ""

    if req.get('form.button.Delete', False):
        deleted = []
        forDel = filter(None, [req.get("defaultSM_%s"% smt,'') \
                                    for smt in smtypes])
        for defsm in forDel:
            parent, delid = portal, defsm
            if '/' in defsm:
                parent_path, delid = defsm.rsplit('/',1)
                parent = portal.restrictedTraverse(parent_path)

            parent.manage_delObjects(ids=[delid,])
            deleted.append(defsm)
        message = "Succesfully deleted: %s" % deleted

    elif req.get('form.button.Default', False):
        pp = getToolByName(context,'portal_properties')
        props = pp.googlesitemap_properties
        default = {}
        for smtype in smtypes:
            defPath = req.get("defaultSM_%s"% smtype, '')
            if defPath:
                pname = "%s_default" % smtype
                props.manage_changeProperties(**{pname : defPath})
                default.update({pname : defPath})
        message = "Succesfully set as default: %s" % default

    elif req.get('form.button.Ping', False):
        pinged = []
        for smtype in smtypes:
            defPath = req.get("defaultSM_%s"% smtype, '')
            if defPath:
                
                #ping_google(portalURL, defPath)
                pinged.append((portalURL, defPath))
        message = "Succesfully pinged: %s" % pinged

return state.set(next_action='traverse_to:string:prefs_gsm_settings',
                 portal_status_message = message)
