##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=trbacks_checked
##title=
##
pw = context.portal_workflow
counter = 0
for trb in trbacks_checked:
    #try:
        obj = context.uid_catalog(UID=trb)[0].getObject()
        pw.doActionFor(obj,'publish')
        counter += 1
    #except:
    #    pass
return state.set(status = 'success', portal_status_message="%s trackbacks published" % (counter))