from pprint import pprint
from operator import itemgetter
from Acquisition import aq_base
from zope.component import getUtility, getMultiAdapter, queryMultiAdapter

from OFS.interfaces import IPropertyManager
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IFolderish
from Products.Archetypes.interfaces import IBaseFolder
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import ILocalPortletAssignmentManager

from plone.memoize import view

try:
    from plone.portlets.interfaces import IPortletAssignmentSettings
except ImportError:
    "Before plon4 we don't have an annotation storage for settings."
    IPortletAssignmentSettings = lambda assignment:{}

from GChartWrapper import VerticalBarStack

COLORS = ['669933', 'CC9966', '993300', 'FF6633', 'E8E4E3', 'A9A486', 'DCB57E', 'FFCC99', '996633', '333300', '00FF00']
OTHER_TYPES = ['Other types']
NO_WF_BIND = 'No workflow'

class OwnershipByType(BrowserView):
    MAX = 10
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.cat = getToolByName(self.context, 'portal_catalog')
        self.users = None
        self.total = None
        self.types = None
        self.data = {}

    def getUsers(self):
        if self.users is None:
            index = self.cat._catalog.getIndex('Creator')
            data = {}
            for k in index._index.keys():
                haslen = hasattr(index._index[k], '__len__')
                if haslen:
                    data[k] = len(index._index[k])
                else:
                    data[k] = 1
            data = data.items()
            data.sort(lambda a, b: a[1] - b[1])
            data.reverse()
            data = data[:self.MAX]
            self.users = [i[0] for i in data]
            self.total = [i[1] for i in data]
        return self.users

    def getTypes(self, all=False):
        if self.types is None:
            index = self.cat._catalog.getIndex('portal_type')
            data = {}
            for k in index._index.keys():
                if not k:
                    continue
                haslen = hasattr(index._index[k], '__len__')
                if haslen:
                    data[k] = len(index._index[k])
                else:
                    data[k] = 1
            data = data.items()
            data.sort(lambda a, b: a[1] - b[1])
            data.reverse()
            self.types = [i[0] for i in data]
        return all and self.types or self.types[:self.MAX]

    def getContent(self, type_):
        if type_ not in self.data:
            data = self.data[type_] = []
            for user in self.getUsers():
                res = self.cat(portal_type=type_, Creator=user)
                l = len(res)
                if l == 0:
                    data.append(0)
                else:
                    data.append(l)
        return self.data[type_]

    def getTotal(self):
        return self.total

    def getChart(self):
        data = []
        types = self.getTypes()
        for type_ in types:
            data.append(self.getContent(type_))
        other = [self.getContent(t) for t in self.getTypes(all=True)[self.MAX:]]
        if other:
            data.append([sum(l) for l in zip(*other)])
        max_value = max(self.getTotal())
        chart = VerticalBarStack(data, encoding='text')
        types = other and types+OTHER_TYPES or types
        chart.title('Content ownership by type').legend(*(types))
        chart.bar('a', 10, 0).legend_pos("b")
        chart.color(*COLORS)
        chart.size(800, 375).scale(0,max_value).axes('xy').label(*self.users)
        chart.axes.type("y")
        chart.axes.range(0,0,max_value)
        return chart.img()

    def getPNG(self):
#        import pdb;
#        pdb.set_trace()
		return '++resource++treemap.png'

class OwnershipByState(BrowserView):
    MAX = 10
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.cat = getToolByName(self.context, 'portal_catalog')
        self.users = None
        self.states = None
        self.total = None
        self.data = {}

    def getUsers(self):
        if self.users is None:
            index = self.cat._catalog.getIndex('Creator')
            data = {}
            for k in index._index.keys():
                haslen = hasattr(index._index[k], '__len__')
                if haslen:
                    data[k] = len(index._index[k])
                else:
                    data[k] = 1
            data = data.items()
            data.sort(lambda a, b: a[1] - b[1])
            data.reverse()
            data = data[:self.MAX]
            self.users = [i[0] for i in data]
            self.total = [i[1] for i in data]
        return self.users

    def getStates(self):
        if self.states is None:
            index = self.cat._catalog.getIndex('review_state')
            data = {}
            for k in index._index.keys():
                haslen = hasattr(index._index[k], '__len__')
                if haslen:
                    data[k] = len(index._index[k])
                else:
                    data[k] = 1
            data = data.items()
            data.sort(lambda a, b: a[1] - b[1])
            data.reverse()
            self.states = [i[0] for i in data]
        return self.states

    def getContent(self, type_):
        if type_ not in self.data:
            if NO_WF_BIND not in self.data:
                self.data[NO_WF_BIND] = self.getTotal()
            data = self.data[type_] = []
            for user in self.getUsers():
                res = self.cat(review_state=type_, Creator=user)
                l = len(res)
                if l == 0:
                    data.append(0)
                else:
                    data.append(l)
            if len(data) > 0:
                self.data[NO_WF_BIND] = map(lambda t,d:t-d, self.data[NO_WF_BIND], data)
        return self.data[type_]

    def getNoWFContentTitle(self):
        return NO_WF_BIND

    def getNoWFContent(self):
        return self.getContent(NO_WF_BIND)

    def getTotal(self):
        if self.total is None:
            self.getUsers()
        return self.total

    def getChart(self):
        data = []
        for state in self.getStates():
            data.append(self.getContent(state))
        data.append(self.getNoWFContent())
        max_value = max(self.getTotal())
        chart = VerticalBarStack(data, encoding='text')
        chart.title('Content ownership by state').legend(*self.states+[NO_WF_BIND])
        chart.bar('a', 10, 0).legend_pos("b")
        chart.color(*COLORS)
        chart.size(800, 375).scale(0,max_value).axes('xy').label(*self.users)
        chart.axes.type("y")
        chart.axes.range(0,0,max_value)
        return chart.img()


class TypeByState(BrowserView):
    MAX = 10
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.cat = getToolByName(self.context, 'portal_catalog')
        self.types = None
        self.states = None
        self.total = None
        self.data = {}

    def getTypes(self):
        if self.types is None:
            index = self.cat._catalog.getIndex('portal_type')
            data = {}
            for k in index._index.keys():
                if not k:
                    continue
                haslen = hasattr(index._index[k], '__len__')
                if haslen:
                    data[k] = len(index._index[k])
                else:
                    data[k] = 1
            data = data.items()
            data.sort(lambda a, b: a[1] - b[1])
            data.reverse()
            self.types = [i[0] for i in data[:self.MAX]]
            self.total = [i[1] for i in data[:self.MAX]]
        return self.types

    def getStates(self):
        if self.states is None:
            index = self.cat._catalog.getIndex('review_state')
            data = {}
            for k in index._index.keys():
                haslen = hasattr(index._index[k], '__len__')
                if haslen:
                    data[k] = len(index._index[k])
                else:
                    data[k] = 1
            data = data.items()
            data.sort(lambda a, b: a[1] - b[1])
            data.reverse()
            self.states = [i[0] for i in data]
        return self.states

    def getContent(self, state):
        if state not in self.data:
            if NO_WF_BIND not in self.data:
                self.data[NO_WF_BIND] = self.getTotal()
            data = self.data[state] = []
            for type_ in self.getTypes():
                res = self.cat(portal_type=type_, review_state=state)
                l = len(res)
                if l == 0:
                    data.append(0)
                else:
                    data.append(l)
            if len(data) > 0:
                self.data[NO_WF_BIND] = map(lambda t,d:t-d, self.data[NO_WF_BIND], data)
        return self.data[state]

    def getTotal(self):
        if self.total is None:
            self.getTypes()
        return self.total

    def getNoWFContentTitle(self):
        return NO_WF_BIND

    def getNoWFContent(self):
        return self.getContent(NO_WF_BIND)

    def getChart(self):
        data = []
        for state in self.getStates():
            data.append(self.getContent(state))
        data.append(self.getContent(NO_WF_BIND))
        max_value = max(self.getTotal())
        chart = VerticalBarStack(data, encoding='text')
        chart.title('Content type by state').legend(*self.states+[NO_WF_BIND])
        chart.bar('a', 10, 0).legend_pos("b")
        chart.color(*COLORS)
        chart.size(800, 375).scale(0,max_value).axes('xy').label(*self.types)
        chart.axes.type("y")
        chart.axes.range(0,0,max_value)
        return chart.img()


class LegacyPortlets(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.total = None
        self.DEBUG = False
        self.expressions = set()

    def _getInfo(self, obj):
        href = obj.absolute_url()
        path = '/'.join(obj.getPhysicalPath())
        info = {
            'path': path,
            'href': href,
            'left_slots': None,
            'right_slots': None,
        }
        if IPropertyManager.providedBy(obj):
            obj = aq_base(obj)
            if obj.hasProperty('left_slots'):
                info['left_slots'] = obj.getProperty('left_slots')
                self.expressions = self.expressions.union(set(info['left_slots']))
            if obj.hasProperty('right_slots'):
                info['right_slots'] = obj.getProperty('right_slots')
                self.expressions = self.expressions.union(set(info['right_slots']))
        return info

    def _walk(self, obj, level=-1):
        yield self._getInfo(obj)
        if level != 0 and (IFolderish.providedBy(obj) or IBaseFolder.providedBy(obj)):
            for v in obj.contentValues():
                for i in self._walk(v, level-1):
                    yield i

    def getPortlets(self):
        level = self.request.form.get('level', 1)
        try:
            level = level and int(level) or 1
        except ValueError:
            level = 1
        infos = []
        for i in self._walk(self.context, level):
            if self.DEBUG or i['left_slots'] is not None or i['right_slots'] is not None:
                infos.append(i)
        self.total = len(infos)
        return infos

    def getTotal(self):
        return self.total

    def getAllPortletExpressions(self):
        exprs = []
        for name in self.expressions:
            name = name.split('|')[0]
            if not '/macros/' in name:
                name = name.split('/')[-1]
            name = name.strip()
            if name not in exprs:
                exprs.append(name)
        exprs.sort()
        return exprs

class PropertiesStats(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.total = None
        self.DEBUG = False
        self.expressions = set()
        self.proplist = []
        self.propname = self.request.form.get('propname') or ""

    def _getInfo(self, obj):

        href = obj.absolute_url()
        path = '/'.join(obj.getPhysicalPath())
        info = {
            'path': path,
            'href': href,
            'slots': None,
        }
        if IPropertyManager.providedBy(obj):
            obj = aq_base(obj)
            self.proplist.extend([i for i in obj.propertyIds() if i not in self.proplist])
            if obj.hasProperty(self.propname):
                info['slots'] = obj.getProperty(self.propname)
                if isinstance(info['slots'], int):
                    info['slots'] = str(info['slots'])
                if not isinstance(info['slots'], basestring):
                    self.expressions = self.expressions.union(set(info['slots']))
                else:
                    self.expressions = self.expressions.union(set([info['slots']]))
        return info

    def _walk(self, obj, level=-1):
        yield self._getInfo(obj)
        if level != 0 and (IFolderish.providedBy(obj) or IBaseFolder.providedBy(obj)):
            for v in obj.contentValues():
                for i in self._walk(v, level-1):
                    yield i

    def getPropsList(self):
        level = self.request.form.get('level', 1)
        try:
            level = level and int(level) or 1
        except ValueError:
            level = 1
        infos = []
        for i in self._walk(self.context, level):
            if self.DEBUG or i['slots'] is not None:
                infos.append(i)
        self.total = len(infos)
        return infos

    def getTotal(self):
        return self.total

    def getAllPortletExpressions(self):
        exprs = []
        for name in self.expressions:
            name = name.strip()
            if name not in exprs:
                exprs.append(name)
        #exprs.sort()
        return exprs

class PortletsStats(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.total = None
        self.DEBUG = False
        self.expressions = set()
        self.proplist = []
        self.propname = self.request.form.get('propname') or ""

    def getAssignmentMappingUrl(self, context, manager):
        baseUrl = str(getMultiAdapter((context, self.request), name='absolute_url'))
        return '%s/++contextportlets++%s' % (baseUrl, manager.__name__)

    def getAssignmentsForManager(self, context, manager):
        assignments = getMultiAdapter((context, manager), IPortletAssignmentMapping)
        return assignments.values()

    def getPortletsMapping(self, context):
        leftcolumn = getUtility(IPortletManager, name=u'plone.leftcolumn', context=context)
        rightcolumn = getUtility(IPortletManager, name=u'plone.rightcolumn', context=context)
        leftmapping = getMultiAdapter((context, leftcolumn,), IPortletAssignmentMapping)
        rightmapping = getMultiAdapter((context, rightcolumn,), IPortletAssignmentMapping)
        return (leftmapping, rightmapping)

    def getLocalPortletsManager(self, context):
        leftcolumn = getUtility(IPortletManager, name='plone.leftcolumn', context=context)
        rightcolumn = getUtility(IPortletManager, name='plone.rightcolumn', context=context)
        leftmanager = getMultiAdapter((context, leftcolumn,), ILocalPortletAssignmentManager)
        rightmanager = getMultiAdapter((context, rightcolumn,), ILocalPortletAssignmentManager)
        return (leftmanager, rightmanager)

    def getPortletsManager(self, context):
        left = getUtility(IPortletManager, name='plone.leftcolumn', context=context)
        right = getUtility(IPortletManager, name='plone.rightcolumn', context=context)
        return (left, right)

    def portlets_for_assignments(self, assignments, manager, base_url):
        data = []
        for idx in range(len(assignments)):
            name = assignments[idx].__name__

            editview = queryMultiAdapter(
                (assignments[idx], self.request), name='edit', default=None)

            if editview is None:
                editviewName = ''
            else:
                editviewName = '%s/%s/edit' % (base_url, name)

            settings = IPortletAssignmentSettings(assignments[idx])

            data.append({
                'title'      : assignments[idx].title,
                'editview'   : editviewName,
                'visible'    : settings.get('visible', True),
                })
        return data

    def getPortlets(self, context, mapping, manager):
        #import pdb; pdb.set_trace()
        return mapping.keys()

    def _getInfo(self, obj):
        href = obj.absolute_url()
        path = '/'.join(obj.getPhysicalPath())
        info = {
            'path': path,
            'href': href,
            'left_slots': None,
            'right_slots': None,
        }
        left, right = self.getPortletsManager(obj)
        #leftmapping, rightmapping = self.getPortletsMapping(obj)
        #leftmanager, rightmanager = self.getLocalPortletsManager(obj)
        #info['left_slots'] = self.getPortlets(obj, leftmapping, leftmanager)
        #info['right_slots'] = self.getPortlets(obj, rightmapping, rightmanager)
        lass = self.getAssignmentsForManager(obj, left)
        rass = self.getAssignmentsForManager(obj, right)
        lurl = self.getAssignmentMappingUrl(obj, left)
        rurl = self.getAssignmentMappingUrl(obj, right)
        plass = self.portlets_for_assignments(lass, left, lurl)
        prass = self.portlets_for_assignments(rass, right, rurl)
        #print obj, plass, prass
        info['left_slots'] = plass #[i['title'] for i in plass]
        info['right_slots'] = prass #[i['title'] for i in prass]
        return info

    def _walk(self, obj, level=-1):
        try:
            yield self._getInfo(obj)
        except:
            pass
        if level != 0 and (IFolderish.providedBy(obj) or IBaseFolder.providedBy(obj)):
            for v in obj.contentValues():
                for i in self._walk(v, level-1):
                    yield i

    def getPropsList(self):
        level = self.request.form.get('level', 1)
        try:
            level = level and int(level) or 1
        except ValueError:
            level = 1
        infos = []
        for i in self._walk(self.context, level):
            if self.DEBUG or i['left_slots'] is not None or i['right_slots'] is not None:
                infos.append(i)
        self.total = len(infos)
        return infos

    def getTotal(self):
        return self.total

    def getAllPortletExpressions(self):
        exprs = []
        for name in self.expressions:
            name = name.strip()
            if name not in exprs:
                exprs.append(name)
        #exprs.sort()
        return exprs

def human_format(num):
    magnitude = 0
    while num >= 1024:
        magnitude += 1
        num /= 1024.0
    # add more suffixes if you need them
    return '%.0f %sB' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

def getSize(brain):
    return float(brain.getObjSize.split()[0])*(
                 brain.getObjSize.endswith('kB') and 1024 \
                 or brain.getObjSize.endswith('MB') and 1024*1024 \
                 or 1)

def matrix_tranform(a):
    b = [0 for i in range(len(a)-1)]
    return [b[:i]+[a[i]]+b[i:] for i in range(len(a))]

class SizeByPath(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.cat = getToolByName(self.context, 'portal_catalog')
        self.purl = getToolByName(self.context, 'portal_url')
        self.total = None
        self.DEBUG = True
        bpath = self.request.form.get('basepath')
        self.basepath = bpath and "/"+bpath.strip("/") or ""
        # set default value for type by size stats
        if not hasattr(self.request, 'type_name'):
            self.request['type_name'] = "File"

    def _brainsByPath(self, path):
        return self.cat(path=path, Language="all")

    def getValidPath(self):
        portal = self.purl.getPortalObject()
        return "/%s%s" % (portal.getId(), self.basepath)

    def getSizeInfoByPath(self):
        """API for chart builder"""
        path = self.getValidPath()
        return [{'size': getSize(b),
                 'type': b.portal_type,
                 'path': b.getPath()} \
                for b in self._brainsByPath(path)]

    def _walk(self, obj, path):
        result = {}
        for b in self._brainsByPath(path):
            bpath = b.getPath()[len(path):]
            p1 = len(bpath)>1 and bpath.split('/')[1] or ''
            if not p1:
                continue
            data = result.setdefault(p1, {'size': 0, 'brain': None})
            data['size'] += getSize(b)
            if b.getPath() == "%s/%s" % (path, p1):
                data['brain'] = b
            result[p1] = data

        self.total = human_format(sum([d['size'] for d in result.values()]))

        sortedres = [(d['size'], d['brain']) for k,d in result.items() if d['brain']]
        sortedres.sort(key=lambda i:i[0], reverse=True)
        return sortedres

    def getInfoForTableItem(self, size, brain):
        oid = brain.getId or brain.id
        analyse_url = ""
        if brain.getObject().isPrincipiaFolderish:
            analyse_url =  "%s/@@size_stats?basepath=%s/%s&submit=Search" % (
                            self.purl(), self.basepath, oid)
        return {'id': oid,
                'path': "%s/%s" % (self.basepath, oid),
                'href': "%s%s/%s" % (self.purl(), self.basepath, oid),
                'human_size': human_format(size),
                'analyse_url': analyse_url,}

    def getTreemapInfo(self):
        path = self.getValidPath()
        return [{'size': size,
                 'type': brain.portal_type,
                 'id': brain.getId or brain.id} \
                for size, brain in self._walk(self.context, path)]

    def getSizeStats(self):
        if self.request.get("submit", None) is None:
            return []

        infos = []
        path = self.getValidPath()
        for size, brain in self._walk(self.context, path):
            if self.DEBUG or size > 1:
                infos.append(self.getInfoForTableItem(size, brain))
        
        return infos

    @view.memoize
    def get_data(self, serh_type="File"):
        if serh_type != "all":
            objects_by_types_info = [i for i in self.getSizeInfoByPath() if i['type']==serh_type]
        else:
            objects_by_types_info = self.getSizeInfoByPath()
        return sorted([ {'h_size': human_format(i['size']), 
                          'size' : i['size'],
                          'path' : i['path'],
                          'id'   : i['path'].split('/')[-1]} 
                        for i in objects_by_types_info ],
                      key=itemgetter('size'),
                      reverse=True)

    def getChart(self):
        type_name = self.request['type_name']
        info_obj = self.get_data(type_name)[:10]
        if not info_obj:
            return "<h2>Not found objetcs of '%s' type</h2>" % type_name
        path, data = zip(*map(itemgetter('path','size'), info_obj))
        max_value = data[0]
        #We need transpozed dataset, matrix_tranform does trabspozition
        chart = VerticalBarStack(matrix_tranform(data))
        chart.title('Objects of "%s" type by size'%type_name)
        chart.bar('a', 10, 0).legend_pos("b")#.legend(*path)
        chart.color(*COLORS)
        chart.size(800, 375).scale(0,max_value)
        chart.axes('xy').axes.type("y").axes.range(0,0,max_value)
        return chart.img()
        
