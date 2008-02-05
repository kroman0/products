import os
from cStringIO import StringIO

from Globals import InitializeClass
from Globals import package_home
from Persistence import PersistentMapping
try:
    from ZODB.PersistentList import PersistentList
except ImportError:
    from persistent.list import PersistentList

from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo

from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.CMFCore.utils import getToolByName, UniqueObject
from Products.CMFCore.Expression import Expression, createExprContext
from Products.CMFCore.CMFCorePermissions import ManagePortal, View

from config import UNIQUE_ID

from zLOG import LOG

_wwwdir = os.path.join(package_home(globals()), 'www')

class MenuItem(SimpleItem):
    """ Element for displaying item in portal tab submenu """

    security = ClassSecurityInfo()

    def __init__(self, title, url=None):
        """ Initialize """
        self._title = title
        self._url = url
        self._menu_items = PersistentList()

    security.declarePublic('getTitle')
    def getTitle(self):
        """ Simple accessor. """
        return self._title

    security.declareProtected(ManagePortal, 'setTitle')
    def setTitle(self, title):
        """ Set menu item's title """
        self._title = title

    security.declarePublic('getUrl')
    def getUrl(self):
        """ Simple accessor. """
        return self._url

    security.declareProtected(ManagePortal, 'setUrl')
    def setUrl(self, url):
        """ Set menu item's url """
        self._url = url

    security.declarePublic('listMenuItems')
    def listMenuItems(self):
        """Get all the menu items in subMenu. """
        return [x.__of__(self) for x in self._menu_items] or []

    security.declareProtected(ManagePortal, 'setSubMenu')
    def setMenuItems(self, items):
        """ Set menu item's subMenu object """
        self._menu_items = PersistentList(items)

    security.declareProtected(ManagePortal, 'addItem')
    def addItem(self, item):
        """ Add MenuItem to _menu_items list """
        self._menu_items.append(item)

    security.declareProtected(ManagePortal, 'deleteItem')
    def deleteItem(self, idx):
        """ Delete MenuItem from _menu_items list """
        return self._menu_items.pop(idx)


InitializeClass(MenuItem)

class DropDownMenuTool(UniqueObject, SimpleItem):

    meta_type = 'DropDownMenu Tool'
    id = UNIQUE_ID
    title="DropDown Menu Tool"

    _submenu_mapping = PersistentMapping()

    security = ClassSecurityInfo()

    manage_options = ({'label' : 'Sub Menus',
                       'action' : 'manage_editSubMenus'},) + SimpleItem.manage_options

    security.declareProtected(ManagePortal, 'manage_editSubMenus')
    manage_editSubMenus = PageTemplateFile('editSubMenus', _wwwdir)

    security.declareProtected(ManagePortal, 'manage_editMenuItems')
    manage_editMenuItems = PageTemplateFile('editMenuItems', _wwwdir)

    security.declareProtected(ManagePortal, 'listPortalTabActions')
    def listPortalTabActions(self):
        """ Return all portal actions with 'portal_tabs' category. """
        result = []
        pu = getToolByName(self, 'plone_utils')
        if hasattr(pu, 'createTopLevelTabs'):
            pactions = getToolByName(self, 'portal_actions').listFilteredActionsFor(self)
            tl_tabs = pu.createTopLevelTabs(pactions)
            for act in tl_tabs:
                data = {'title': act['name'],
                        'id':act['id'],
                        'actionExpression': act['url']}
                result.append(data)
        else:
            portal = getToolByName(self, 'portal_url').getPortalObject()
            portal_act = getToolByName(self, 'portal_actions')
            actions = portal_act._cloneActions()

            for act in actions:
                if act.category == 'portal_tabs':
                    data = {'title': act.title,
                             'id': act.id,
                             'actionExpression': \
                             Expression(act.getActionExpression())(createExprContext(portal, portal, portal))}
                    result.append(data)
        return result

    security.declareProtected(ManagePortal, 'generateSubMenuMapping')
    def generateSubMenuMapping(self):
        """  Create top-level subMenu mapping. """
        mapping = self._submenu_mapping
        #for item in mapping.keys():
            #for tab in self.listPortalTabActions():
                #if item == tab['title']:
                    #present = True
                    #break
                #else: present = False
            #if not present: del mapping[item]
        for tab in self.listPortalTabActions():
            if tab['title'] not in mapping.keys():
                mapping[tab['title']] = PersistentList()
        self._submenu_mapping = mapping
        return self._submenu_mapping

    security.declareProtected('View', 'getValueByKey')
    def getValueByKey(self, key):
        """  Return value from _submenu_mapping for given key """
        try:
            return [item.__of__(self) for item in self._submenu_mapping[key]]
        except KeyError:
            return None

    security.declareProtected(ManagePortal, 'validateTitle')
    def validateTitle(self, title):
        """ Safeguard against empty (later duplicate ;) title. """
        if not title:
            raise ValueError, 'Please, enter title'
        else: return 1

    security.declareProtected(ManagePortal, 'getSubMenuByPath')
    def getSubMenuByPath(self, submenu_path):
        """ Return submenu for a given submenu_path """
        if submenu_path in self._submenu_mapping.keys():
            return self.getValueByKey(submenu_path)
        else:
            #LOG('getSubMenuByPath', 111, 'afterElseSubmenuPath', str(submenu_path))
            return self.getMenuItemByPath(submenu_path).listMenuItems()

    security.declareProtected(ManagePortal, 'getMenuItemByPath')
    def getMenuItemByPath(self, submenu_path):
        """ Return menuitem for a given submenu_path """
        path = submenu_path.strip().split('/')
        menuitem = self.getValueByKey(path[0])[int(path[1])]
        for i in path[2:]:
            menuitem = menuitem.listMenuItems()[int(i)]
        return menuitem

    security.declareProtected(ManagePortal, 'getBreadcrumbs')
    def getBreadcrumbs(self, submenu_path):
        """ Return breadcrumbs dictionary for listMenuItems form """
        path = submenu_path.split('/')
        result  = [{'title' : path[0],
                    'url'   : '%s/manage_editMenuItems?submenu_path=%s'%(self.absolute_url(), path[0])},]
        for i in range(len(path[1:])):
            temp_path = '/'.join(path[:i+2])
            result.append({'title' : self.getMenuItemByPath(temp_path).getTitle(),
                            'url'   : '%s/manage_editMenuItems?submenu_path=%s'%(self.absolute_url(), temp_path)})
        return result

    #security.declareProtected(ManagePortal, 'getLevel')
    #def getLevel(self, submenu, space, lst):
        #if submenu != None:
    ##        if submenu.listMenuItems() != ():
            #space += '    '
            #for menuitem in submenu.listMenuItems():
                #lst += space + menuitem.getTitle() + '  ==  ' + str(menuitem.getSubMenu()) + '\n'
                #lst = str(self.getLevel(menuitem.getSubMenu(), space, lst))
            #return lst
        #else: return lst

    #security.declareProtected(ManagePortal, 'getMenuTree')
    #def getMenuTree(self):
        #""" Return all submenu with it's menuitems """
        #out = '\n'
        #mapping = self._submenu_mapping
        #for item in mapping.items():
            #space = ''
            #out += space + item[0] + '  ---  ' + str(item[1]) + '\n'
            #if item[1] != '':
                #out += space + str(self.getValueByKey(item[0])) + '\n' + str(self.getLevel(self.getValueByKey(item[0]), space, lst=''))
        #return out

    security.declareProtected(ManagePortal, 'manage_addMenuItem')
    def manage_addMenuItem(self, submenu_path, title, url=None, REQUEST=None):
        """ Add MenuItem via ZMI """
        self.validateTitle(title)
        if submenu_path in self._submenu_mapping.keys():
            self._submenu_mapping[submenu_path].append(MenuItem(title, url))
        else:
            self.getMenuItemByPath(submenu_path).addItem(MenuItem(title, url))

        if REQUEST:
            REQUEST['RESPONSE'].redirect( '%s/manage_editMenuItems'
                                          '?submenu_path=%s&manage_tabs_message=MenuItem+\'%s\'+added.'
                                        % (self.absolute_url(), submenu_path, title))

    security.declareProtected(ManagePortal, 'manage_removeMenuItem')
    def manage_removeMenuItem(self, submenu_path, REQUEST=None):
        """ Remove MenuItem via ZMI """
        path = submenu_path.strip().split('/')
        if len(path)==2:
            self._submenu_mapping[path[0]].pop(int(path[1]))
        elif len(path)>2:
            self.getMenuItemByPath('/'.join(path[:-1])).deleteItem(int(path[-1]))

        if REQUEST:
            REQUEST['RESPONSE'].redirect( '%s/manage_editMenuItems'
                                          '?submenu_path=%s&manage_tabs_message=MenuItem+removed.'
                                        % (self.absolute_url(), '/'.join(path[:-1])))

    security.declareProtected(ManagePortal, 'manage_saveMenuItems')
    def manage_saveMenuItems(self, submenu_path, REQUEST=None):
        """  Save MenuItems for given subMenu via ZMI. """
        records = REQUEST.get('menuitems')
        if submenu_path in self._submenu_mapping.keys():
            submenu = self._submenu_mapping[submenu_path]
        else:
            submenu = self.getSubMenuByPath(submenu_path)
        if records and len(records) == len(submenu):
             for i in range(len(submenu)):
                 if records[i].get('title'): submenu[i].setTitle(records[i].get('title'))
                 submenu[i].setUrl(records[i].get('url'))

        if REQUEST:
            REQUEST['RESPONSE'].redirect('%s/manage_editMenuItems'
                                         '?&submenu_path=%s&manage_tabs_message=MenuItems+updated.'
                                        % (self.absolute_url(), submenu_path))

    security.declareProtected(ManagePortal, 'manage_moveMenuItemDown')
    def manage_moveMenuItemDown(self, submenu_path, REQUEST=None):
        """ Move the MenuItem down via ZMI """
        path = submenu_path.strip().split('/')
        if len(path)==2:
            self._submenu_mapping[path[0]] = PersistentList(self.moveItem(path[1], int(path[1])+1, self._submenu_mapping[path[0]]))
        elif len(path)>2:
            menuitem = self.getMenuItemByPath('/'.join(path[:-1]))
            menuitem.setMenuItems(list(self.moveItem(path[-1], int(path[-1])+1, menuitem.listMenuItems())))

        if REQUEST:
            REQUEST['RESPONSE'].redirect('%s/manage_editMenuItems'
                                         '?&submenu_path=%s&manage_tabs_message=MenuItem+moved+up.'
                                        % (self.absolute_url(), '/'.join(path[:-1])))

    security.declareProtected(ManagePortal, 'manage_moveMenuItemUp')
    def manage_moveMenuItemUp(self, submenu_path, REQUEST=None):
        """ Move the MenuItem up via ZMI """
        path = submenu_path.strip().split('/')
        if len(path)==2:
            self._submenu_mapping[path[0]] = PersistentList(self.moveItem(path[1], int(path[1])-1, self._submenu_mapping[path[0]]))
        elif len(path)>2:
            menuitem = self.getMenuItemByPath('/'.join(path[:-1]))
            menuitem.setMenuItems(list(self.moveItem(path[-1], int(path[-1])-1, menuitem.listMenuItems())))

        if REQUEST:
            REQUEST['RESPONSE'].redirect('%s/manage_editMenuItems'
                                         '?&submenu_path=%s&manage_tabs_message=MenuItem+moved+up.'
                                        % (self.absolute_url(), '/'.join(path[:-1])))

    security.declareProtected(ManagePortal, 'moveItem')
    def moveItem(self, index, position, menuitems):
        """ Move an item to the given position."""
        if index == position:
            return
        elif position < 0:
            position = 0
        menuitems = list(menuitems)
        menuitem = menuitems.pop(int(index))
        menuitems.insert(int(position), menuitem)
        return menuitems

    security.declareProtected(ManagePortal, 'manage_reorderItems')
    def manage_reorderItems(self, idxs, submenu_path):
        """ Reorder menu items of the same submenu in given order """
        path = submenu_path.strip().split('/')
        submenu = self.reorderItems(idxs, self.getSubMenuByPath(submenu_path))
        if len(path) == 1:
            self._submenu_mapping[path[0]] = PersistentList(submenu)
        elif len(path) > 1:
            menuitem = self.getMenuItemByPath(submenu_path)
            menuitem.setMenuItems(submenu)

    security.declareProtected(ManagePortal, 'reorderItems')
    def reorderItems(self, idxs, submenu):
        """ Return list in given order """
        idxs = list(map(int,idxs))
        #if len(idxs) != len(submenu): return False
        return [submenu[idx] for idx in idxs]

InitializeClass(DropDownMenuTool)
