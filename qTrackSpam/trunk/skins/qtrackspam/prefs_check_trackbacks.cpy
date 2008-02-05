##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from zLOG import LOG
res = context.portal_catalog(portal_type='TrackBack', review_state='pending',sort_on='Date')
trbacks = [r.getObject() for r in res]
blacklisted =[]
trackspam = context.portal_trackspam
for trback in trbacks:
    if not trackspam.checkURL(trback.getUrl()):
        blacklisted.append(trback.UID())
return state.set(status = 'success', blacklisted = blacklisted)