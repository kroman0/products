from zope.event import notify
from Products.qPloneGoogleSitemaps.events import AfterTransitionEvent

def pingGoogleSitemap(stch):
    notify(AfterTransitionEvent(stch.object,
           stch.workflow, stch.old_state, stch.new_state,
           stch.transition, stch.status, stch.kwargs))
    return 0