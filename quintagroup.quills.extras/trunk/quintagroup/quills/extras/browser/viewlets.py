from plone.app.viewletmanager.manager import BaseOrderedViewletManager
from quills.core.interfaces.enabled import IWeblogEnhanced

class ConditionalViewletManager(BaseOrderedViewletManager):

    def render(self):
        if not IWeblogEnhanced.providedBy(self.context):
            return super(ConditionalViewletManager, self).render()
        return u''
