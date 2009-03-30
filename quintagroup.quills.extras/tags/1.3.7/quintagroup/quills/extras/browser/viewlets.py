from zope import interface
from plone.app.viewletmanager.manager import BaseOrderedViewletManager
from quills.core.interfaces.enabled import IWeblogEnhanced
from quills.core.interfaces import ITopicContainer, ITopic
from quintagroup.quills.extras.browser.interfaces import IWeblogCategory

class ConditionalViewletManager(BaseOrderedViewletManager):

    FILTER_INTERFACES = set([ITopic, IWeblogEnhanced, IWeblogCategory])
    def render(self):
        iprovided = set(list(interface.providedBy(self.context)))
        if iprovided.intersection(self.FILTER_INTERFACES):
            return u''
        return super(ConditionalViewletManager, self).render()
        
