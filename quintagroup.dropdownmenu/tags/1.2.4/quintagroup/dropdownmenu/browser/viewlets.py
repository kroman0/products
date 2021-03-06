# -*- coding: utf-8 -*-
from Acquisition import aq_inner

from zope.component import getMultiAdapter

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IAction, IActionCategory
from Products.CMFCore.ActionInformation import ActionInfo
from Products.CMFPlone.utils import versionTupleFromString

from plone.memoize.instance import memoize
from plone.memoize.compress import xhtmlslimmer
from plone.app.layout.viewlets import common
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.navigation.interfaces import INavtreeStrategy

from quintagroup.dropdownmenu.browser.menu import DropDownMenuQueryBuilder
from quintagroup.dropdownmenu.util import getDropDownMenuSettings

from time import time
from plone.memoize import ram
import copy


def menu_cache_key(f, view):
    portal_state = getMultiAdapter((view.context, view.request),
                                   name=u'plone_portal_state')
    site_len = len(portal_state.navigation_root_path().split('/'))
    content_path = view.context.getPhysicalPath()[site_len:]
    if view.conf.content_tabs_level > 0:
        content_path = content_path[:view.conf.content_tabs_level]
    path_key = '/'.join(content_path)
    return view.__name__ + \
           path_key + \
           str(time() // (60 * 5))  # Every five minutes
                                    # Note that the HTTP RAM-cache
                                    # typically purges entries after
                                    # 60 minutes.


def tabs_cache_key(f, view, site_url):
    return site_url + str(time() // (60 * 60))


def dropdowncache(f):
    def func(view):
        if view.conf.show_actions_tabs:
            return f(view)
        return ram.cache(menu_cache_key)(f)(view)
    return func


class GlobalSectionsViewlet(common.GlobalSectionsViewlet):
    index = ViewPageTemplateFile('templates/sections.pt')
    recurse = ViewPageTemplateFile('templates/sections_recurse.pt')

    def update(self):
        # we may need some previously defined variables
        #super(GlobalSectionsViewlet, self).update()

        # prepare to gather portal tabs
        context = aq_inner(self.context)
        self.conf = self._settings()
        self.tool = getToolByName(context, 'portal_actions')
        self.site_url = getToolByName(context, 'portal_url')()
        self.context_state = getMultiAdapter((self.context, self.request),
                                              name="plone_context_state")
        self.context_url = self.context_state.is_default_page() and \
            '/'.join(self.context.absolute_url().split('/')[:-1]) or \
            self.context.absolute_url()

        self.cat_sufix = self.conf.nested_category_sufix or ''
        self.cat_prefix = self.conf.nested_category_prefix or ''

    @property
    def portal_tabs(self):
        tabs = []

        # fetch actions-based tabs?
        if self.conf.show_actions_tabs:
            tabs.extend(self._actions_tabs())

        # fetch content structure-based tabs?
        if self.conf.show_content_tabs:
            # put content-based actions before content structure-based ones?
            if self.conf.content_before_actions_tabs:
                tabs = self._content_tabs() + tabs
            else:
                tabs.extend(self._content_tabs())

        return tabs

    def _actions_tabs(self):
        """Return tree of tabs based on portal_actions tool configuration"""
        conf = self.conf
        tool = self.tool

        # check if we have required root actions category inside tool
        if conf.actions_category not in tool.objectIds():
            return []
        listtabs = []
        res, listtabs = self.prepare_tabs(self.site_url)
        res = copy.deepcopy(res)
        self.tabs = listtabs

        # if there is no custom menu in portal tabs return
        if not listtabs:
            return []

        current_item = -1
        delta = 1000
        for info in listtabs:
            if  self.context_url.startswith(info['url']) and \
                len(self.context_url) - len(info['url']) < delta:
                delta = len(self.context_url) - len(info['url'])
                current_item = listtabs.index(info)
        self.id_chain = []

        if current_item > -1 and current_item < len(listtabs) and \
            (listtabs[current_item]['url'] != self.site_url or \
            listtabs[current_item]['url'] == self.site_url and \
            self.context_url == self.site_url):

            self.mark_active(listtabs[current_item]['id'],
                             listtabs[current_item]['url'])

        self._activate(res)
        return res

    @ram.cache(tabs_cache_key)
    def prepare_tabs(self, site_url):
        def normalize_actions(category, object, level, parent_url=None):
            """walk through the tabs dictionary and build list of all tabs"""
            tabs = []
            for info in self._actionInfos(category, object):
                icon = info['icon'] and '<img src="%s" />' % info['icon'] or ''
                children = []
                bottomLevel = self.conf.actions_tabs_level
                if bottomLevel < 1 or level < bottomLevel:
                    # try to find out appropriate subcategory
                    subcat_id = self.cat_prefix + info['id'] + self.cat_sufix
                    if subcat_id != info['id'] and \
                       subcat_id in category.objectIds():
                        subcat = category._getOb(subcat_id)
                        if IActionCategory.providedBy(subcat):
                            children = normalize_actions(subcat, object,
                                                         level + 1,
                                                         info['url'])

                parent_id = category['id'].replace(self.cat_prefix,
                                '').replace(self.cat_sufix, '')
                tab = {'id': info['id'],
                   'title': info['title'],
                   'url': info['url'],
                   'parent': (parent_id, parent_url)}
                tabslist.append(tab)

                tab = {'id': info['id'],
                       'Title': info['title'],
                       'Description': info['description'],
                       'getURL': info['url'],
                       'show_children': len(children) > 0,
                       'children': children,
                       'currentItem': False,
                       'currentParent': False,
                       'item_icon': {'html_tag': icon},
                       'normalized_review_state': 'visible'}
                tabs.append(tab)
            return tabs
        tabslist = []
        tabs = normalize_actions(self.tool._getOb(self.conf.actions_category),
                                 aq_inner(self.context), 0)
        return tabs, tabslist

    def _activate(self, res):
        """Mark selected chain in the tabs dictionary"""
        for info in res:
            if info['getURL'] in self.id_chain:
                info['currentItem'] = True
                info['currentParent'] = True
                if info['children']:
                    self._activate(info['children'])

    def mark_active(self, current_id, url):
        for info in self.tabs:
            if info['id'] == current_id and info['url'] == url:
                self.mark_active(info['parent'][0], info['parent'][1])
                self.id_chain.append(info['url'])

    def _actionInfos(self, category, object, check_visibility=1,
                     check_permissions=1, check_condition=1, max=-1):
        """Return action infos for a given category"""
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

    @dropdowncache
    def createMenu(self):
        html = self.recurse(children=self.portal_tabs, level=1)
        return xhtmlslimmer.compress(html)

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
