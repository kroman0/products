# -*- coding: utf-8 -*-
from Acquisition import aq_inner

from zope.component import getMultiAdapter, getUtility

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IAction, IActionCategory
from Products.CMFCore.ActionInformation import ActionInfo
from Products.CMFPlone.utils import versionTupleFromString

from plone.memoize.instance import memoize
from plone.app.layout.viewlets import common
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder

from quintagroup.dropdownmenu.interfaces import IDropDownMenuSettings
from quintagroup.dropdownmenu.browser.menu import DropDownMenuQueryBuilder
from quintagroup.dropdownmenu.util import getDropDownMenuSettings


class GlobalSectionsViewlet(common.GlobalSectionsViewlet):
    index = ViewPageTemplateFile('templates/sections.pt')
    recurse = ViewPageTemplateFile('templates/sections_recurse.pt')


    def update(self):
        # we may need some previously defined variables
        #super(GlobalSectionsViewlet, self).update()

        # prepare to gather portal tabs
        tabs = []
        context = aq_inner(self.context)
        self.conf = conf = self._settings()
        self.tool = getToolByName(context, 'portal_actions')
        self.site_url = getToolByName(context, 'portal_url')()
        self.context_state = getMultiAdapter((self.context, self.request), 
                                              name="plone_context_state")
        self.context_url =  self.context_state.is_default_page() and \
            '/'.join(self.context.absolute_url().split('/')[:-1]) or \
            self.context.absolute_url()

        # fetch actions-based tabs?
        if conf.show_actions_tabs:
            tabs.extend(self._actions_tabs())

        # fetch content structure-based tabs?
        if conf.show_content_tabs:
            # put content-based actions before content structure-based ones?
            if conf.content_before_actions_tabs:
                tabs = self._content_tabs() + tabs
            else:
                tabs.extend(self._content_tabs())

        # assign collected tabs eventually
        self.portal_tabs = tabs

    def _actions_tabs(self):
        """Return tree of tabs based on portal_actions tool configuration"""
        conf = self.conf
        tool = self.tool
        context = aq_inner(self.context)

        # check if we have required root actions category inside tool
        if conf.actions_category not in tool.objectIds():
            return []

        self.chain = []  #save not traversable chain here
        self.tchain = []  #save the best traversable chain here
        self.res, c = self._subactions(tool._getOb(conf.actions_category), context, 0, self.chain)
        self.tchain.reverse()
        self.chain.reverse()
        self.chain = self.chain and self.chain or self.tchain
        self._activate(self.res)
        return self.res
    
    def _activate(self, res, level=0):
        """Mark selected chain in the tabs dictionary"""
        if self.chain and len(self.chain) > level:
            res[self.chain[level]]['currentItem'] = True
            res[self.chain[level]]['currentParent'] = True
            if level + 1 < len(self.chain):
                self._activate(res[self.chain[level]]['children'], level+1)


    def _subactions(self, category, object, level=0, lchain=[]):
        """Build tabs dictionary out of portal actions"""
        tabs = []
        currentParentId = -1
        index = -1
        local = False      
        for info in self._actionInfos(category, object):
            # prepare data for action
            # TODO: implement current element functionality, maybe should be
            #       done on a template level because of separate content and
            #       actions tabs are rendered separately

            index += 1
            icon = info['icon'] and '<img src="%s" />' % info['icon'] or ''
    
            if  self.context_url.startswith(info['url']) and info['url'] != self.site_url:
                if currentParentId > -1:
                    if len(tabs[currentParentId]['getURL']) < len(info['url']): 
                        currentParentId = index
                else:
                    currentParentId = index
            if  self.context_url == info['url']:
                lchain.append(index)
                local = True
                
            # look up children for a given action
            children = []
            bottomLevel = self.conf.actions_tabs_level
            if bottomLevel < 1 or level < bottomLevel:
                # try to find out appropriate subcategory
                subcat_id = info['id']
                if self.conf.nested_category_sufix is not None:
                    subcat_id += self.conf.nested_category_sufix
                if self.conf.nested_category_prefix is not None:
                    subcat_id = self.conf.nested_category_prefix + subcat_id
                if subcat_id != info['id'] and \
                   subcat_id in category.objectIds():
                    subcat = category._getOb(subcat_id)
                    if IActionCategory.providedBy(subcat):
                        children, local = self._subactions(subcat, object, level+1, lchain)
                        if local:
                            lchain.append(index)
            
            # make up final tab dictionary
            tab = {'Title': info['title'],
                   'Description': info['description'],
                   'getURL': info['url'],
                   'show_children': len(children) > 0,
                   'children': children,
                   'currentItem': False, 
                   'currentParent': False,
                   'item_icon': {'html_tag': icon},
                   'normalized_review_state': 'visible'}
            tabs.append(tab)

        if currentParentId > -1:
            self.tchain.append(currentParentId)
        return tabs, local

    def _actionInfos(self, category, object, check_visibility=1,
                     check_permissions=1, check_condition=1, max=-1):
        """Return action infos for a given category"""
        context = aq_inner(self.context)
        ec = self.tool._getExprContext(object)
        actions = [ActionInfo(action, ec) for action in category.objectValues()
                    if IAction.providedBy(action)]

        action_infos = []
        for ai in actions:
            if check_visibility and not ai['visible']:
                continue
            if check_permissions and not ai['allowed']:
                continue
            if check_condition and not ai['available']:
                continue
            action_infos.append(ai)
            if max + 1 and len(action_infos) >= max:
                break
        return action_infos

    def _content_tabs(self):
        """Return tree of tabs based on content structure"""
        context = aq_inner(self.context)

        queryBuilder = DropDownMenuQueryBuilder(context)
        strategy = getMultiAdapter((context, None), INavtreeStrategy)
        # XXX This works around a bug in plone.app.portlets which was
        # fixed in http://dev.plone.org/svn/plone/changeset/18836
        # When a release with that fix is made this workaround can be
        # removed and the plone.app.portlets requirement in setup.py
        # be updated.
        if strategy.rootPath is not None and strategy.rootPath.endswith("/"):
            strategy.rootPath = strategy.rootPath[:-1]

        return buildFolderTree(context, obj=context, query=queryBuilder(),
                               strategy=strategy).get('children', [])

    @memoize
    def _settings(self):
        """Fetch dropdown menu settings registry"""
        return getDropDownMenuSettings(self.context)

    def createMenu(self):
        return self.recurse(children=self.portal_tabs, level=1)

    def _old_update(self):
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        actions = context_state.actions()
        portal_tabs_view = getMultiAdapter((self.context, self.request),
                                           name='portal_tabs_view')
        self.portal_tabs = portal_tabs_view.topLevelTabs(actions=actions)

        selectedTabs = self.context.restrictedTraverse('selectedTabs')
        self.selected_tabs = selectedTabs('index_html',
                                          self.context,
                                          self.portal_tabs)
        self.selected_portal_tab = self.selected_tabs['portal']

    @memoize
    def is_plone_four(self):
        """Indicates if we are in plone 4.
        
        """
        pm = getToolByName(aq_inner(self.context), 'portal_migration') 
        try:
            version = versionTupleFromString(pm.getSoftwareVersion())
        except AttributeError:
            version = versionTupleFromString(pm.getFileSystemVersion())

        if version:
            return version[0] == 4

