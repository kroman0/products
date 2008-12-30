from Products.CMFCore.utils import getToolByName
from Products.ResourceRegistries.browser.styles import StylesView as base

class StylesView(base):
    """ Information for style rendering. """

    def styles(self):
        styles = super(StylesView, self).styles()
        portal_url = getToolByName(self.context, 'portal_url')
        new_url = portal_url()
        portal_url = portal_url.getPortalObject().absolute_url()
        for style in styles:
            src = style.get('src', '')
            if src != '':
                style['src'] = src.replace(portal_url, new_url, 1)
        return styles
