from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from plone.app.portlets.storage import PortletAssignmentMapping

from quintagroup.portlet.collection import collection

from quintagroup.portlet.collection.tests.base import TestCase


from Products.CMFCore.utils import getToolByName


class TestQPortletCollection(TestCase):
    def afterSetUp(self):
        self.setRoles(('Manager',))

    def testPortletTypeRegistered(self):
        portlet = getUtility(
            IPortletType, name='quintagroup.portlet.collection.Collection')
        self.assertEquals(
            portlet.addview, 'quintagroup.portlet.collection.Collection')

    def testInterfaces(self):
        portlet = collection.Assignment(header=u"title")
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portlet = getUtility(
            IPortletType, name='quintagroup.portlet.collection.Collection')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={'header': u"test title"})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], collection.Assignment))

    def testInvokeEditView(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = collection.Assignment(header=u"title")
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, collection.EditForm))

    def testRenderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = collection.Assignment(header=u"title")

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, collection.Renderer))


class TestQPortletCollectionRenderer(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager',))
        self.pages = self._createType(self.folder, 'Topic', 'pages')
        crit = self.folder.pages.addCriterion(
            'portal_type', 'ATSimpleStringCriterion')
        crit.setValue('Document')

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = assignment or collection.Assignment(header=u"title")

        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def _createType(self, context, portal_type, id, **kwargs):
        """Helper method to create a new type
        """
        ttool = getToolByName(context, 'portal_types')
        cat = self.portal.portal_catalog

        fti = ttool.getTypeInfo(portal_type)
        fti.constructInstance(context, id, **kwargs)
        obj = getattr(context.aq_inner.aq_explicit, id)
        cat.indexObject(obj)
        return obj

    def test_collection_path_unicode(self):
        """
        Cover problem in #9184
        """
        r = self.renderer(
            context=self.portal,
            assignment=collection.Assignment(header=u"title",
                                             target_collection=u"/events"))
        r = r.__of__(self.folder)
        self.assertEqual(r.collection().id, 'events')

    def test_portletStyle(self):
        renderer = self.renderer(context=self.portal,
                                 assignment=collection.Assignment(
                                     header=u"title",
                                     styling="TestClass"))
        renderer = renderer.__of__(self.folder)
        renderer.update()

        self.failUnless('TestClass' in renderer.render())

    def test_attributes(self):
        page = self._createType(self.folder, 'Document', 'page')
        page.update(title="Test Page", description="Test description")
        target_collection = '/Members/test_user_1_/pages'
        renderer = self.renderer(context=self.portal,
                                 assignment=collection.Assignment(
                                     header=u"title",
                                     item_attributes=[u'Title'],
                                     target_collection=target_collection))
        renderer = renderer.__of__(self.folder)
        renderer.update()
        self.failUnless('Test Page' in renderer.render())
        self.failUnless('Test description' not in renderer.render())


class TestQPortletCollectionQuery(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager',))
        #make a collection
        self.collection = self._createType(self.folder, 'Topic', 'collection')

    def _createType(self, context, portal_type, id, **kwargs):
        """Helper method to create a new type
        """
        ttool = getToolByName(context, 'portal_types')
        cat = self.portal.portal_catalog

        fti = ttool.getTypeInfo(portal_type)
        fti.constructInstance(context, id, **kwargs)
        obj = getattr(context.aq_inner.aq_explicit, id)
        cat.indexObject(obj)
        return obj

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.leftcolumn', context=self.portal)
        assignment = assignment
        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def testSimpleQuery(self):
        # set up our collection to search for Folders
        crit = self.folder.collection.addCriterion(
            'portal_type', 'ATSimpleStringCriterion')
        crit.setValue('Folder')

        # add a few folders
        for i in range(6):
            self.folder.invokeFactory('Folder', 'folder_%s' % i)
            getattr(self.folder, 'folder_%s' % i).reindexObject()

        # the folders are returned by the topic
        collection_num_items = len(self.folder.collection.queryCatalog())
        # We better have some folders
        self.failUnless(collection_num_items >= 6)

        mapping = PortletAssignmentMapping()
        t_collection = '/Members/test_user_1_/collection'
        mapping['foo'] = collection.Assignment(header=u"title",
                                               target_collection=t_collection)
        collectionrenderer = self.renderer(context=None, request=None,
                                           view=None, manager=None,
                                           assignment=mapping['foo'])

        # we want the portlet to return us the same results as the collection
        self.assertEquals(
            collection_num_items, len(collectionrenderer.results()))

    def testRandomQuery(self):
        # we're being perhaps a bit too clever in random mode with the
        # internals of the LazyMap returned by the collection query, so let's
        # try a bunch of scenarios to make sure they work

        def reset_memoize(inst):
            # Decorator memoize adds attribute('_memojito_') to class instance.
            # It has cached function and their values so it should be deleted
            # for testing.
            # Extra info: http://codereview.corp.quintagroup.com/171241/show
            if hasattr(inst, '_memojito_'):
                delattr(inst, '_memojito_')

        # set up our portlet renderer
        mapping = PortletAssignmentMapping()
        t_collection = '/Members/test_user_1_/collection'
        mapping['foo'] = collection.Assignment(header=u"title",
                                               random=True,
                                               target_collection=t_collection)
        collectionrenderer = self.renderer(context=None, request=None,
                                           view=None, manager=None,
                                           assignment=mapping['foo'])

        # add some folders
        for i in range(6):
            self.folder.invokeFactory('Folder', 'folder_%s' % i)
            getattr(self.folder, 'folder_%s' % i).reindexObject()

        # collection with no criteria -- should return empty list, without
        # error
        self.assertEqual(len(collectionrenderer.results()), 0)
        reset_memoize(collectionrenderer)

        # let's make sure the results aren't being memoized
        old_func = self.folder.collection.queryCatalog
        global collection_was_called
        collection_was_called = False

        def mark_collection_called(**kw):
            global collection_was_called
            collection_was_called = True
        self.folder.collection.queryCatalog = mark_collection_called
        collectionrenderer.results()
        reset_memoize(collectionrenderer)
        self.folder.collection.queryCatalog = old_func
        self.failUnless(collection_was_called)

        # collection with simple criterion -- should return 1 (random) folder
        crit = self.folder.collection.addCriterion(
            'portal_type', 'ATSimpleStringCriterion')
        crit.setValue('Folder')
        self.assertEqual(len(collectionrenderer.results()), 1)
        reset_memoize(collectionrenderer)

        # collection with multiple criteria -- should behave similarly
        crit = self.folder.collection.addCriterion(
            'Creator', 'ATSimpleStringCriterion')
        crit.setValue('test_user_1_')
        collectionrenderer.results()

        # collection with sorting -- should behave similarly (sort is
        # ignored internally)
        self.folder.collection.setSortCriterion('modified', False)
        self.assertEqual(len(collectionrenderer.results()), 1)
        reset_memoize(collectionrenderer)

        # same criteria, now with limit set to 2 -- should return 2 (random)
        # folders
        collectionrenderer.data.limit = 2
        self.assertEqual(len(collectionrenderer.results()), 2)
        reset_memoize(collectionrenderer)

        # make sure there's no error if the limit is greater than the # of
        # results found
        collectionrenderer.data.limit = 10
        self.failUnless(len(collectionrenderer.results()) >= 6)
        reset_memoize(collectionrenderer)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestQPortletCollection))
    suite.addTest(makeSuite(TestQPortletCollectionRenderer))
    suite.addTest(makeSuite(TestQPortletCollectionQuery))
    return suite
