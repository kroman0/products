from Products.CMFCore.utils import getToolByName
from Products.ResourceRegistries.browser.kss import KSSView as base

class KSSView(base):
    """ Information for kss rendering. """

    def kineticstylesheets(self):
        ksses = super(KSSView, self).kineticstylesheets()
        portal_url = getToolByName(self.context, 'portal_url')
        new_url = portal_url()
        portal_url = portal_url.getPortalObject().absolute_url()
        for kss in ksses:
            src = kss.get('src', '')
            if src != '':
                kss['src'] = src.replace(portal_url, new_url, 1)
        return ksses

