import unittest
import pprint
import os

from zope.testing import doctest, cleanup
from zope.component import provideUtility, provideAdapter, adapts
from zope.interface import classProvides, implements

from collective.transmogrifier.interfaces import ISectionBlueprint, ISection
from collective.transmogrifier.tests import tearDown
from collective.transmogrifier.sections.tests import sectionsSetUp
from collective.transmogrifier.sections.tests import SampleSource

from Products.Five import zcml

import quintagroup.transmogrifier
from quintagroup.transmogrifier.xslt import stylesheet_registry

# Doctest support

class DataPrinter(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.printkey = [i.strip() for i in options['print'].splitlines() if i.strip()]
        if 'prettyprint' in options:
            self.pprint = pprint.PrettyPrinter().pprint

    def __iter__(self):
        for item in self.previous:
            if self.printkey:
                data = item
                for i in self.printkey:
                    if i in data:
                        data = data[i]
                    else:
                        data = None
                        break
                if data is not None:
                    if hasattr(self, 'pprint'):
                        self.pprint(data)
                    else:
                        print data
            yield item

ctSectionsSetup = sectionsSetUp
def sectionsSetUp(test):
    ctSectionsSetup(test)
    # load meta.zcml of directives that are used in out package config
    import Products.GenericSetup
    zcml.load_config('meta.zcml', Products.GenericSetup)
    zcml.load_config('configure.zcml', quintagroup.transmogrifier)

    provideUtility(DataPrinter,
        name=u'quintagroup.transmogrifier.tests.dataprinter')

def siteWalkerSetUp(test):
    sectionsSetUp(test)

    from Products.CMFCore.interfaces import IFolderish
    from Products.Archetypes.interfaces import IBaseFolder

    class MockContent(object):
        path = ()

        def getPhysicalPath(self):
            return self.path

        def getPortalTypeName(self):
            return self.__class__.__name__

    class Document(MockContent):
        pass

    class Folder(MockContent, dict):
        implements(IBaseFolder)

        contentItems = dict.items
        contentValues = dict.values

    class MockPortal(MockContent, dict):
        implements(IFolderish)

        contentItems = dict.items
        contentValues = dict.values

    portal = MockPortal()

    test.globs['plone'] = portal
    test.globs['transmogrifier'].context = test.globs['plone']

    portal.path = ('', 'plone')
    portal['document1'] = Document()
    portal['document1'].path = ('', 'plone', 'document1')
    portal['folder1'] = Folder()
    portal['folder1'].path = ('', 'plone', 'folder1')
    portal['folder1']['document2'] = Document()
    portal['folder1']['document2'].path = ('', 'plone', 'folder1', 'document2')
    portal['folder1']['folder2'] = Folder()
    portal['folder1']['folder2'].path = ('', 'plone', 'folder1', 'folder2')
    portal['document3'] = Document()
    portal['document3'].path = ('', 'plone', 'document3')

def manifestSetUp(test):
    sectionsSetUp(test)

    item = {'_entries' : (
        ('document1', 'Document'),
        ('folder1', 'Folder'),
        ('document3', 'Document'),)
    }

    class ManifestSource(SampleSource):
        classProvides(ISectionBlueprint)
        implements(ISection)

        def __init__(self, *args, **kw):
            super(ManifestSource, self).__init__(*args, **kw)
            self.sample = (item, dict())

    provideUtility(ManifestSource,
        name=u'quintagroup.transmogrifier.tests.manifestsource')

    from quintagroup.transmogrifier.manifest import ManifestSection
    section = ManifestSection(test.globs['transmogrifier'], 
        'manifest', {'blueprint': ''}, iter(()))
    data = section.createManifest(item['_entries'])
    test.globs['data'] = data

def marshallSetUp(test):
    sectionsSetUp(test)

    from Products.Archetypes.interfaces import IBaseObject

    class MockCriterion(object):
        implements(IBaseObject)

    class MockPortal(object):
        implements(IBaseObject)

        _last_path = None
        def unrestrictedTraverse(self, path, default):
            if path[0] == '/':
                return default # path is absolute
            if isinstance(path, unicode):
                return default
            if path == 'not/existing/bar':
                return default
            if path == 'topic/criterion':
                self._last_path = path
                return MockCriterion()
            if path.endswith('/notatcontent'):
                return object()
            self._last_path = path
            return self

        def getId(self):
            return "plone"

        exported = ()
        def marshall(self, instance, **kwargs):
            self.exported += ((self._last_path, kwargs.get('atns_exclude')),)
            # Marshall often fails to export topic criteria
            if isinstance(instance, MockCriterion):
                return None, None, None
            else:
                return None, None, "marshalled"

    portal = MockPortal()
    test.globs['plone'] = portal
    test.globs['transmogrifier'].context = test.globs['plone']

    from Products.Marshall import registry
    def getComponent(name):
        return portal
    registry.getComponent = getComponent

    class MarshallSource(SampleSource):
        classProvides(ISectionBlueprint)
        implements(ISection)

        def __init__(self, *args, **kw):
            super(MarshallSource, self).__init__(*args, **kw)
            self.sample = (
                dict(_path='spam/eggs/foo', _excluded_fields=('fieldone','fieldtwo')),
                dict(_path='topic/criterion'),
                dict(_path='not/existing/bar'),
                dict(),
                dict(_path='spam/eggs/notatcontent'),
            )
    provideUtility(MarshallSource,
        name=u'quintagroup.transmogrifier.tests.marshallsource')

def propertyManagerSetUp(test):
    sectionsSetUp(test)

    from OFS.interfaces import IPropertyManager

    class MockPortal(object):
        implements(IPropertyManager)

        _last_path = None
        def unrestrictedTraverse(self, path, default):
            if path[0] == '/':
                return default # path is absolute
            if isinstance(path, unicode):
                return default
            if path == 'not/existing/bar':
                return default
            if path.endswith('/notatcontent'):
                return object()
            self._last_path = path
            return self

        updated = ()
        def _propertyMap(self):
            self.updated += (self._last_path,)
            return ({'id':'propone', 'type': 'string', 'mode': 'w'},
                    {'id':'proptwo', 'type': 'string', 'mode': 'w'},
                    {'id':'propthree', 'type': 'string', 'mode': 'w'},
                    {'id':'propfour', 'type': 'string', 'mode': 'w'})

        def getProperty(id, d=None):
            return 'value'

    portal = MockPortal()
    test.globs['plone'] = portal
    test.globs['transmogrifier'].context = test.globs['plone']

    class PropertyManagerSource(SampleSource):
        classProvides(ISectionBlueprint)
        implements(ISection)

        def __init__(self, *args, **kw):
            super(PropertyManagerSource, self).__init__(*args, **kw)
            self.sample = (
                dict(_path='spam/eggs/foo', _excluded_properties=('proptwo','propthree')),
                dict(_path='not/existing/bar'),
                dict(),
                dict(_path='spam/eggs/notatcontent'),
            )

    provideUtility(PropertyManagerSource,
        name=u'quintagroup.transmogrifier.tests.propertymanagersource')

def discussionContainerSetUp(test):
    sectionsSetUp(test)

    class MockDiscussionItem(object):
        def __init__(self, reply, text):
            self.in_reply_to = reply
            self.text = text

        def Creator(self):
            return "creator"

        def ModificationDate(self):
            return "date"

        def getMetadataHeaders(self):
            return []

    class MockPortal(object):
        discussion = {
            '1': MockDiscussionItem(None, 'comment to content'),
            '2': MockDiscussionItem('1', 'reply to first comment'),
            '3': MockDiscussionItem(None, 'other comment to content')
        }

        @property
        def talkback(self):
            return self

        def objectItems(self):
            l = self.discussion.items()
            l.sort(key=lambda x: int(x[0]))
            return l

        def unrestrictedTraverse(self, path, default):
            if path[0] == '/':
                return default # path is absolute
            if isinstance(path, unicode):
                return default
            if path == 'not/existing/bar':
                return default
            if path.endswith('/notdiscussable'):
                return object()
            return self

    portal = MockPortal()
    test.globs['plone'] = portal
    test.globs['transmogrifier'].context = test.globs['plone']

    import Acquisition
    def aq_base(obj):
        return obj
    Acquisition.aq_base = aq_base

    class DiscussionContainerSource(SampleSource):
        classProvides(ISectionBlueprint)
        implements(ISection)

        def __init__(self, *args, **kw):
            super(DiscussionContainerSource, self).__init__(*args, **kw)
            self.sample = (
                dict(_path='spam/eggs/foo'),
                dict(_path='not/existing/bar'),
                dict(),
                dict(_path='spam/eggs/notdiscussable'),
            )

    provideUtility(DiscussionContainerSource,
        name=u'quintagroup.transmogrifier.tests.discussioncontainersource')


def dataCorrectorSetUp(test):
    sectionsSetUp(test)

    class MockPortal(object):
        def unrestrictedTraverse(self, path, default):
            if path[0] == '/':
                return default # path is absolute
            if isinstance(path, unicode):
                return default
            if path == 'not/existing/bar':
                return default
            if path.endswith('/notadaptable'):
                return object()
            return self

    portal = MockPortal()
    test.globs['plone'] = portal
    test.globs['transmogrifier'].context = test.globs['plone']

    from quintagroup.transmogrifier.interfaces import IExportDataCorrector, \
        IImportDataCorrector

    class MockExportAdapter(object):
        implements(IExportDataCorrector)
        adapts(MockPortal)
        def __init__(self, context):
            self.context = context

        def __call__(self, data):
            return "modified export data"

    provideAdapter(MockExportAdapter, name="marshall")

    class MockImportAdapter(object):
        implements(IImportDataCorrector)
        adapts(MockPortal)
        def __init__(self, context):
            self.context = context

        def __call__(self, data):
            return "modified import data"

    provideAdapter(MockImportAdapter, name="manifest")

    class DataCorrectorSource(SampleSource):
        classProvides(ISectionBlueprint)
        implements(ISection)

        def __init__(self, *args, **kw):
            super(DataCorrectorSource, self).__init__(*args, **kw)
            self.sample = (
                dict(),
                dict(_files=dict(marshall="item hasn't path")),
                dict(_path='spam/eggs/foo'),
                dict(_path='not/existing/bar'),
                dict(_path='spam/eggs/notadaptable', _files=dict(marshall="object isn't adaptable")),
                dict(_path='spam/eggs/foo',
                     _files=dict(marshall='marshall data', unchanged='this must be unchanged')),
                dict(_path='spam/eggs/foo',
                     _files=dict(manifest='manifest data', unchanged='this must be unchanged')),
            )

    provideUtility(DataCorrectorSource,
        name=u'quintagroup.transmogrifier.tests.datacorrectorsource')

def writerSetUp(test):
    sectionsSetUp(test)

    class MockExportContext(object):
        def __init__( self, *args, **kwargs):
            self.args = args
            for k, v in kwargs.items():
                setattr(self, k, v)
            self._wrote = []

        def __getitem__(self, name):
            return getattr(self, name, None)

        def __contains__(self, name):
            return hasattr(self, name)

        def writeDataFile(self, filename, text, content_type, subdir=None):
            filename = '%s/%s' % (subdir, filename)
            self._wrote.append((filename, text, content_type))

        def __repr__(self):
            s = " ".join(["%s=%s" % (k,v) for k,v in self.__dict__.items()])
            return "<%s %s>" % (self.__class__.__name__, s)


    from Products.GenericSetup import context

    context.DirectoryExportContext = type('Directory', (MockExportContext,), {})
    context.TarballExportContext = type('Tarball', (MockExportContext,), {})
    context.SnapshotExportContext = type('Snapshot', (MockExportContext,), {})

    from Products.CMFCore import utils
    def getToolByName(context, tool_id):
        return context
    utils.getToolByName = getToolByName

    class WriterSource(SampleSource):
        classProvides(ISectionBlueprint)
        implements(ISection)

        def __init__(self, *args, **kw):
            super(WriterSource, self).__init__(*args, **kw)
            self.sample = (
                dict(_path='spam/eggs/foo'),
                dict(_files=dict(mock=dict(name='.first.xml', data='some data'))),
                dict(_path='spam/eggs/foo',
                     _files=dict(mock=dict(name='.first.xml', data='some data'),
                                 other=dict(name='.second.xml', data='other data'))),
                dict(_path='other/path',
                     _files=dict(mock=dict(name='.third.xml', data='some data')))
            )

    provideUtility(WriterSource,
        name=u'quintagroup.transmogrifier.tests.writersource')

    class SingleItemSource(SampleSource):
        classProvides(ISectionBlueprint)
        implements(ISection)

        def __init__(self, *args, **kw):
            super(SingleItemSource, self).__init__(*args, **kw)
            self.sample = (
                dict(_path='', _files={}),
            )

    provideUtility(SingleItemSource,
        name=u"quintagroup.transmogrifier.tests.singleitemsource")

def readerSetUp(test):
    sectionsSetUp(test)

    class MockImportContext(object):

        _dirs = [
            'structure',
            'structure/news', 'structure/news/recent',
            'structure/pages', 'structure/pages/front-page',
        ]
        _files = [
            'structure/.properties.xml',
            'structure/other.file',
            'structure/news/.objects.xml',
            'structure/pages/.objects.xml',
            'structure/pages/front-page/.marshall.xml',
            'structure/pages/front-page/.comments.xml',
        ]

        def __init__( self, *args, **kwargs):
            self.args = args
            for k, v in kwargs.items():
                setattr(self, k, v)

        def __repr__(self):
            s = " ".join(["%s=%s" % (k,v) for k,v in self.__dict__.items()])
            return "<%s %s>" % (self.__class__.__name__, s)

        def readDataFile(self, filename, subdir=None):
            return 'some data'

        def isDirectory(self, path):
            return path == '' or path in self._dirs

        def listDirectory(self, path):
            all_names = self._dirs + self._files
            if path:
                pfx_len = len(path)+1
            else:
                pfx_len = 0
            names = []
            for name in all_names:
                if name == path:
                    continue
                if not name.startswith(path):
                    continue
                name = name[pfx_len:]
                if '/' in name:
                    continue
                names.append(name)
            return names

    from Products.GenericSetup import context

    context.DirectoryImportContext = type('Directory', (MockImportContext,),
        {'listDirectory': lambda self, path: []})
    context.TarballImportContext = type('Tarball', (MockImportContext,), {})
    context.SnapshotImportContext = type('Snapshot', (MockImportContext,),
        {'listDirectory': lambda self, path: []})

    from Products.CMFCore import utils
    def getToolByName(context, tool_id):
        return context
    utils.getToolByName = getToolByName

def manifestImportSetUp(test):
    sectionsSetUp(test)

    man1 = """<?xml version="1.0" ?>
<manifest>
  <record type="Document">document1</record>
  <record type="Folder">folder1</record>
</manifest>
"""

    man2 = """<?xml version="1.0" ?>
<manifest>
  <record type="Document">document2</record>
  <record type="Document">document3</record>
</manifest>
"""

    item1 = dict(
        _path='',
        _files=dict(
            manifest=dict(
                name='.objects.xml',
                data=man1
            )
        )
    )

    item2 = dict(
        _path='document1',
    )

    item3 = dict(
        _path='folder1',
        _files=dict(
            manifest=dict(
                name='.objects.xml',
                data=man2
            )
        )
    )

    item4 = dict(
        _path='folder1/document2',
    )

    item5 = dict(
        _path='document4',
    )

    class ManifestSource(SampleSource):
        classProvides(ISectionBlueprint)
        implements(ISection)

        def __init__(self, *args, **kw):
            super(ManifestSource, self).__init__(*args, **kw)
            self.sample = (item1, dict(), item2, item3, item4, item5)

    provideUtility(ManifestSource,
        name=u'quintagroup.transmogrifier.tests.manifestsource')

def substitutionSetUp(test):
    sectionsSetUp(test)

    class SubstitutionSource(SampleSource):
        classProvides(ISectionBlueprint)
        implements(ISection)

        def __init__(self, *args, **kw):
            super(SubstitutionSource, self).__init__(*args, **kw)
            self.sample = (
                {},
                {'_type': 'Blog'},
                {'_type': 'PloneFormMailer'},
                {'_type': 'Document'},
            )

    provideUtility(SubstitutionSource,
        name=u'quintagroup.transmogrifier.tests.substitutionsource')

class MetaDirectivesTests(unittest.TestCase):
    def setUp(self):
        zcml.load_config('meta.zcml', quintagroup.transmogrifier)

    def tearDown(self):
        stylesheet_registry.clear()
        cleanup.cleanUp()

    def testEmptyZCML(self):
        zcml.load_string('''\
<configure xmlns:transmogrifier="http://namespaces.plone.org/transmogrifier">
</configure>''')
        self.assertEqual(stylesheet_registry.listStylesheetNames(), ())

    def testConfigZCML(self):
        zcml.load_string('''\
<configure
    xmlns:transmogrifier="http://namespaces.plone.org/transmogrifier">
<transmogrifier:stylesheet
    source="marshall"
    from="Blog"
    to="Weblog"
    file="blog.xsl"
    />
</configure>''')
        self.assertEqual(stylesheet_registry.listStylesheetNames(),
                         (u'marshall:Blog:Weblog',))
        path = os.path.split(quintagroup.transmogrifier.__file__)[0]
        self.assertEqual(
            stylesheet_registry.getStylesheet('marshall', 'Blog', 'Weblog'),
            dict(from_=u'Blog',
                 to=u'Weblog',
                 file=os.path.join(path, 'blog.xsl'))
        )

    def testMultipleZCML(self):
        zcml.load_string('''\
<configure
    xmlns:transmogrifier="http://namespaces.plone.org/transmogrifier">
<transmogrifier:stylesheet
    source="marshall"
    from="Blog"
    to="Weblog"
    file="blog.xsl"
    />
<transmogrifier:stylesheet
    source="propertymanager"
    from="BlogEntry"
    to="WeblogEntry"
    file="blogentry.xsl"
    />
</configure>''')
        self.assertEqual(stylesheet_registry.listStylesheetNames(),
                         (u'marshall:Blog:Weblog', u'propertymanager:BlogEntry:WeblogEntry'))

def xsltSetUp(test):
    sectionsSetUp(test)

    class XSLTSource(SampleSource):
        classProvides(ISectionBlueprint)
        implements(ISection)

        def __init__(self, *args, **kw):
            super(XSLTSource, self).__init__(*args, **kw)
            self.sample = (
                {},
                {'_type': 'Weblog'},
                {'_old_type': 'Blog'},
                {'_old_type': 'Blog',
                 '_type': 'Weblog',
                 '_files': {'manifest': {'data': 'xml', 'name': 'manifest.xml'}}},
                {'_old_type': 'Blog',
                 '_type': 'Weblog',
                 '_files': {'marshall': {'data': 'xml', 'name': 'marshall.xml'}}},
            )

    provideUtility(XSLTSource,
        name=u'quintagroup.transmogrifier.tests.xsltsource')

    from quintagroup.transmogrifier.xslt import XSLTSection, stylesheet_registry

    XSLTSection.applyTransformations = lambda self, xml, xslt: 'transformed xml'
    test.globs['stylesheet_registry'] = stylesheet_registry

def test_suite():
    import sys
    suite = unittest.findTestCases(sys.modules[__name__])
    suite.addTests((
        doctest.DocFileSuite(
            'sitewalker.txt',
            setUp=siteWalkerSetUp, tearDown=tearDown),
        doctest.DocFileSuite(
            'manifest.txt',
            setUp=manifestSetUp, tearDown=tearDown),
        doctest.DocFileSuite(
            'marshall.txt',
            setUp=marshallSetUp, tearDown=tearDown),
        doctest.DocFileSuite(
            'propertymanager.txt',
            setUp=propertyManagerSetUp, tearDown=tearDown),
        doctest.DocFileSuite(
            'discussioncontainer.txt',
            setUp=discussionContainerSetUp, tearDown=tearDown),
        doctest.DocFileSuite(
            'datacorrector.txt',
            setUp=dataCorrectorSetUp, tearDown=tearDown),
        doctest.DocFileSuite(
            'writer.txt',
            setUp=writerSetUp, tearDown=tearDown),
        doctest.DocFileSuite(
            'reader.txt',
            setUp=readerSetUp, tearDown=tearDown),
        doctest.DocFileSuite(
            'manifest_import.txt',
            setUp=manifestImportSetUp, tearDown=tearDown),
        doctest.DocFileSuite(
            'substitution.txt',
            setUp=substitutionSetUp, tearDown=tearDown),
        doctest.DocFileSuite(
            'xslt.txt',
            setUp=xsltSetUp, tearDown=tearDown),
    ))
    return suite
