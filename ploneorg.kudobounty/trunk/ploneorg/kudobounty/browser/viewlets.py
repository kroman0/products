from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

from ploneorg.kudobounty.config import TOPIC_PATH

# -*- extra stuff goes here -*-

class BountyViewlet(common.ViewletBase):
    render = ViewPageTemplateFile('bounty_viewlet.pt')

    def topic(self):
        try:
            return self.portal_state.portal().restrictedTraverse(TOPIC_PATH)
        except KeyError:
            return None

    def available(self):
        return bool(self.topic())

    def bounty_submissions(self):
        #import pdb;pdb.set_trace()
        query = self.topic().queryCatalog()
        res = [{'url':b.getRemoteUrl,
                'title': b.Title,
                'alt': b.Description,
                'img_url': "%s/image_bounty" % b.getURL()} \
                 for b in query]
        return res
