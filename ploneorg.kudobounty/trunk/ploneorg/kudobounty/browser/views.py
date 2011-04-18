from DateTime import DateTime
from zope.interface import implements, Interface
from zope.component import queryUtility
from zope.component import getMultiAdapter
from plone.i18n.normalizer.interfaces import IURLNormalizer

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.config import RENAME_AFTER_CREATION_ATTEMPTS

from ploneorg.kudobounty import logger
from ploneorg.kudobounty.config import *
from ploneorg.kudobounty import kudobountyMessageFactory as _


class BountyFormProcessorView(BrowserView):
    """
    test_view browser view
    """

    @property
    def portal(self):
        return getMultiAdapter((self.context, self.request),
                               name='plone_portal_state').portal()

    @property
    def wftool(self):
        return getMultiAdapter((self.context, self.request),
                               name='plone_tools').workflow()

    def __call__(self):
        """
        test method
        """
        try:
            container = self.portal.restrictedTraverse(SUBMISSION_CONTAINER_ID)
        except:
            logger.warn("Can't find bounty submission container " \
               "with '%s' path" % SUBMISSION_CONTAINER_ID)
        else:
            # Create Bounty Program Submission object
            form = self.request.form
            title = ' '.join(filter(None,
                        [form['firstName'], form['lastName'], form['organization']]))
            id = self.getUniqueId(container, title)
            container.invokeFactory("Bounty Program Submission", id)
            bps = getattr(container, id)
            # Update Submission with data from the PFG form
            form['image'] = form['image_file']
            form['description'] = form['altText']
            effd, expd = self.getEffExpDates()
            form['effectiveDate'] = effd
            form['expirationDate'] = expd
            
            bps.update(**form)
            bps.unmarkCreationFlag()
            bps.reindexObject()
            # Change wf state
            self.wftool.doActionFor(bps, "submit")

        return {}

    def getEffExpDates(self):
        now = DateTime()
        month = now.month()
        year = now.year()
        if month == 12:
            month = 1
            year = year + 1
        else:
            month = month + 1
        effd = DateTime(year, month, 1, 0, 0)
        expd = DateTime(year, month + 1, 1, 23, 55) - 1
        return effd, expd
        

    def getUniqueId(self, container, title):
        id = queryUtility(IURLNormalizer).normalize(title)
        container_ids = container.objectIds()
        check_id = lambda id, required: id in container_ids

        invalid_id = check_id(id, required=1)
        if not invalid_id:
            return id

        idx = 1
        while idx <= RENAME_AFTER_CREATION_ATTEMPTS:
            new_id = "%s-%d" % (id, idx)
            if not check_id(new_id, required=1):
                return new_id
            idx += 1

        return None
