#
# PATCH DEFERRED CONTENT RULE EXECUTION ON ADDING AT OBJECTS
#
# this behavior not suite for testing quills because of
# in tests it uses addEntry method, which perform adding
# blog post with only one invokeFactory method without
# following steps (performed in TTW plone operation)
#

from plone.app.contentrules import handlers as pcrh
def patched_added(event):
    """When an object is added, execute rules assigned to its new parent.

    There is special handling for Archetypes objects.
    """
    if pcrh.is_portal_factory(event.object):
        return

    # The object added event executes too early for Archetypes objects.
    # We need to delay execution until we receive a subsequent IObjectInitializedEvent

    pcrh.init()
    pcrh.execute(event.newParent, event)

pcrh.added = patched_added
