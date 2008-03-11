from zope.interface import Interface

class IPloneTabsControlPanel(Interface):
    """ Configlet for managing portal_actions, quintagroup.plonetabs """
    
    def getPageTitle(category='portal_tabs'):
        """ Return Title for configlet page for given category """
    
    def hasActions(category="portal_tabs"):
        """ Whether there are actions in portal_actions with given category """
    
    def getPortalActions(category="portal_tabs"):
        """ Return portal actions with given category """
    
    def isGeneratedTabs():
        """ Whether disable_folder_section field is turned off """
    
    def isNotFoldersGenerated():
        """ Whether disable_nonfolderish_sections field is turned off """
    
    def getActionsList(category="portal_tabs"):
        """ Return html code for actions list with given category """
    
    def getGeneratedTabs():
        """ Return html code for autogenerated tabs """
    
    def getRootTabs():
        """ Return portal root elements """
    
    def getCategories():
        """ Return list of categories contained in portal_actions tool """
    
    def test(condition, ifTrue, ifFalse):
        """ Instead of test function in skins page templates """
    
