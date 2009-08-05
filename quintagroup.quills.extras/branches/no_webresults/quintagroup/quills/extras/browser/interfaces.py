# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager
from quills.core.interfaces.enabled import IPossibleWeblog

class IActionsBox(IViewletManager):
    """A viewlet manager for collect actions
    """

class IWeblogCategory(IPossibleWeblog):
    """Marker interface for Blog' category folder
    """

class IQuillsExtrasLayer(Interface):
    """A layer specific to quintagroup.quills.extras package
    """
