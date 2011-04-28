from DateTime import DateTime
from zope.interface import implements, Interface
from zope.component import getUtility, queryUtility
from zope.component import getMultiAdapter
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from plone.i18n.normalizer.interfaces import IURLNormalizer
from plone.registry.interfaces import IRegistry

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.config import RENAME_AFTER_CREATION_ATTEMPTS

from ploneorg.kudobounty import logger
from ploneorg.kudobounty.config import *
from ploneorg.kudobounty import kudobountyMessageFactory as _

from collective.portlet.collectionmultiview.renderers.base import (
                                    CollectionMultiViewBaseRenderer)

class BountyCollectionRenderer(CollectionMultiViewBaseRenderer):
    __name__ = 'Bounty Collection View'
    template = ViewPageTemplateFile('bounty_collection_view.pt')

    @property
    def available(self):
        # Render only on the portal context and there are some results
        context_state = getMultiAdapter((self.context, self.request),
                                        name='plone_context_state')
        return context_state.is_portal_root() and len(self.results())

    def bounty_form_url(self):
        # Prepare bounty-form url based on plone.registry record
        portal_url = getMultiAdapter((self.context, self.request),
                                      name='plone_portal_state').portal_url()
        form_path = getUtility(IRegistry)['ploneorg.kudobounty.bountySubmissionForm']
        return "%s/%s" % (portal_url, form_path)


class BountyFormProcessorView(BrowserView):
    """
    Browser page view for automation of 'Bounty Program Submission'
    content object creation.
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
        Perform following steps:
          * Fill it with data from the PFG form,
          * Set effective and expiration date to nearest month
          * Change the workflow state into pending state
        """
        try:
            container = self.portal.restrictedTraverse(CONTAINER_ID)
        except:
            msg = "Can't find bounty submission container"
            logger.warn(msg + " with '%s' path" % CONTAINER_ID)
            raise RuntimeError(msg)
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
        # NOTE:
        # Mixed and little refactored functions of
        # Products.Archetypes.BaseObject.BaseObject class:
        #  * _findUniqueId (check uniqueness of id in the container)
        #  * generateNewId (used url noralizer utility)
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
