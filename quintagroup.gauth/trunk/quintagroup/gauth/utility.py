"""
    Provide utility for getting GData portal account email and password.
"""

import logging
import gdata.service
from zope.interface import implements
from zope.component import queryMultiAdapter, queryAdapter
from plone.memoize.view import memoize_contextless

from quintagroup.gauth.interfaces import IGAuthUtility
from quintagroup.gauth.browser.configlet import IGAuthConfigletSchema

logger = logging.getLogger('quintagroup.gauth')
def logException(msg, context=None):
    logger.exception(msg)
    if context is not None:
        error_log = getattr(context, 'error_log', None)
        if error_log is not None:
            error_log.raising(sys.exc_info())

class GAuthUtility(object):
    implements(IGAuthUtility)

    gconf = None
    
    def __init__(self, context):
        # Bind utility to the context
        pps = queryMultiAdapter((context, context.REQUEST), name="plone_portal_state")
        self.gconf = queryAdapter(pps.portal(), IGAuthConfigletSchema)

    @property
    def email(self):
        """ Get the email."""
        return getattr(self.gconf, 'gauth_email', '')

    @property
    def password(self):
        """ Get the password."""
        return getattr(self.gconf, 'gauth_pass', '')


class SafeQuery(object):
    """ Base class for perform safe Google data service calls,
        with automatic programming re-loginning.

        So if class need automatic relogin to Google Date services, it must
        inherit from the class and use safeQuery metho to call to services methods

        For example ...

        class MyGdataService(SafeQuery):

            def __init__(self):
                gauth_util = queryUtility(IGAuthUtility)
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
            if hasattr(serv, 'ProgrammaticLogin'):
                logException("Token Expired -> Update it.")
                serv.ProgrammaticLogin()
                return meth(*margs, **mkwargs)
            else:
                raise

