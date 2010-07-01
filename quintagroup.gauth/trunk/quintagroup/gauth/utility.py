"""
    Provide utility for getting GData portal account email and password.
"""

from zope.interface import implements
from zope.component import queryMultiAdapter, queryAdapter
from plone.memoize.view import memoize_contextless

from quintagroiup.gauth.interfaces import IGAuthInterface
from quintagroup.gdata.browser.configlet import IGDataConfigletSchema


class GAuthUtility(object):
    implements(IGAuthInterface)

    def __init__(self, context):
        self.context = context

    @property
    @memoize_contextless
    def gdataconf(self):
        pps = queryMultiAdapter((self.context, self.context.REQUEST), name="plone_portal_state")
        return queryAdapter(pps.portal(), IGDataConfigletSchema)

    @property
    def email(self):
        """ Get the email."""
        return self.gdataconf.gdata_email

    @property
    def password(self):
        """ Get the password."""
        return self.gdataconf.gdata_pass


    # @property
    # @memoize_contextless
    # def portal(self):
    #     pps = queryMultiAdapter((self.context, self.context.REQUEST), name="plone_portal_state")
    #     return pps.portal()
