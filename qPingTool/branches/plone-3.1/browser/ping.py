from Acquisition import aq_inner
from Products.qPingTool import qPingToolMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class PingView(BrowserView):
    """A class with helper methods for use in views/templates.
    """
    template = ViewPageTemplateFile('ping_setup.pt')
    ping_message = ''

    def __call__(self):
        postback = True
        context = aq_inner(self.context)
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        portal_pingtool = getToolByName(portal, 'portal_pingtool')
        form = self.request.form
        ping = form.get('form.button.Ping', False)
        setup_save = form.get('form.button.Save', False)
        setup_cancel = form.get('form.button.Cancel', False)
        if ping:
            status, message = portal_pingtool.pingFeedReader(context)
            point = message.find('.')+1
            self.ping_message = message[point:]
            state = self.get_state(status)
            portal.plone_utils.addPortalMessage(message[:point], state)

        elif setup_save:
            enable_ping = form.get('enable_ping', False)
            ping_sites = form.get('ping_sites', ())
            ping_Weblog = form.get('ping_Weblog', '')
            ping_RSS1 = form.get('ping_RSS1', '')
            ping_RSS2 = form.get('ping_RSS2', '')
            status, message = portal_pingtool.setupPing(context, enable_ping, ping_sites, ping_Weblog, ping_RSS1, ping_RSS2)
            state = self.get_state(status)
            portal.plone_utils.addPortalMessage(_(message), state)

        elif setup_cancel:
            portal.plone_utils.addPortalMessage(_("Changes canceled."))
            self.request.response.redirect(context.absolute_url())
            postback = False

        if postback:
            return self.template()

    def get_state(self, status):
        if status == 'success':
            state = 'info'
        elif status == 'failed':
            state = 'warning'
        else:
            state = 'info'
        return state
