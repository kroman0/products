"""
    Provide utility for getting GData portal account email and password.
"""

import logging
from zope.interface import implements
from zope.component import queryMultiAdapter, queryAdapter
from plone.memoize.view import memoize_contextless

from quintagroup.gauth.interfaces import IGAuthInterface
from quintagroup.gauth.browser.configlet import IGAuthConfigletSchema

logger = logging.getLogger('quintagroup.gauth')
def logException(msg, context=None):
    logger.exception(msg)
    if context is not None:
        error_log = getattr(context, 'error_log', None)
        if error_log is not None:
            error_log.raising(sys.exc_info())

class GAuthUtility(object):
    implements(IGAuthInterface)

    gconf = None

    def gconf_init(self, context, request):
        pps = queryMultiAdapter((context, request), name="plone_portal_state")
        self.gconf = queryAdapter(pps.portal(), IGAuthConfigletSchema)

    @property
    def email(self):
        """ Get the email."""
        if not self.gconf:
            return None
        return self.gconf.gauth_email

    @property
    def password(self):
        """ Get the password."""
        if not self.gconf:
            return None
        return self.gconf.gauth_pass


class SafeQuery(object):
    """ Base class for perform safe Google data service calls,
        with automatic programming re-loginning.

        So if class need automatic relogin to Google Date services, it must
        inherit from the class and use safeQuery metho to call to services methods

        For example ...

        class MyGdataService(SafeQuery):

            def __init__(self):
                gauth_util = queryUtility(IGAuthInterface)
                self.service = gdata.spreadsheet.service.SpreadsheetService(
                                   gauth_util.email, gauth_util.password)
                self.service.ProgrammaticLogin()

            def fooservice(self):
                ...
                self.safeQuery(self.service, self.service.GetSpreadsheetsFeed,
                               title="some title")
                ...

        So call to fooservice should automatic relogin to SpreadsheetService even
        if token expired.
    """

    def safeQuery(self, serv, meth, *margs, **mkwargs):
        try:
            return meth(*margs, **mkwargs)
        except gdata.service.RequestError, e:
            logException("Token Expired -> Update it.")
            if hasattr(serv, 'ProgrammaticLogin'):
                serv.ProgrammaticLogin()
                return meth(*margs, **mkwargs)
            else:
                raise

