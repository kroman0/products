from zope.interface import Interface, Attribute


class IPloneTabsControlPanel(Interface):
    """Configlet for managing portal_actions, quintagroup.plonetabs"""

    prefix = Attribute('prefix', 'Prefix to apply on edit forms')
    sufix = Attribute('sufix', 'Sufix to apply on edit forms')

    def getPageTitle(category='portal_tabs'):
        """Return Title for configlet page for given category"""

    def hasActions(category="portal_tabs"):
        """Whether there are actions in portal_actions with given category"""

    def getPortalActions(category="portal_tabs"):
        """Return portal actions with given category"""

    def isGeneratedTabs():
        """Whether disable_folder_section field is turned off"""

    def isNotFoldersGenerated():
        """Whether disable_nonfolderish_sections field is turned off"""

    def getActionsList(category="portal_tabs"):
        """Return html code for actions list with given category"""

    def getAutoGenereatedSection(cat_name, errors):
        """Return html code for all autogenerated section"""

    def getGeneratedTabs():
        """Return html code for autogenerated tabs"""

    def getRootTabs():
        """Return portal root elements"""

    def getCategories():
        """Return list of categories contained in portal_actions tool"""

    def portal_tabs():
        """See global-sections viewlet"""

    def selected_portal_tab():
        """See global-sections viewlet"""

    def test(condition, ifTrue, ifFalse):
        """Instead of test function in skins page templates"""