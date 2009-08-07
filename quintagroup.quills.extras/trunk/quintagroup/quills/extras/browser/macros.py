# -*- coding: utf-8 -*-
from quills.app.browser.macros import *

class HeaderMacros(Macros):
    template = ViewPageTemplateFile('quills_header_macros.pt')

class WeblogEntryMacros(Macros):
    template = ViewPageTemplateFile('quills_entry_macros.pt')

class WeblogMacros(Macros):
    template = ViewPageTemplateFile('quills_weblog_macros.pt')
