from Products.CMFCore.utils import getToolByName
from Products.ResourceRegistries.browser.scripts import ScriptsView as base

class ScriptsView(base):
    """ Information for script rendering. """

    def scripts(self):
        scripts = super(ScriptsView, self).scripts()
        portal_url = getToolByName(self.context, 'portal_url')
        new_url = portal_url()
        portal_url = portal_url.getPortalObject().absolute_url()
        for script in scripts:
            src = script.get('src', '')
            if src != '':
                script['src'] = src.replace(portal_url, new_url, 1)
        return scripts
