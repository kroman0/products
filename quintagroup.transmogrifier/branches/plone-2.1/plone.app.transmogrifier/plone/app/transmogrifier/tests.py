import unittest

import collective.transmogrifier.zopex3

from zope.component import provideUtility
from zope.interface import classProvides, implements
from zope.testing import doctest
from collective.transmogrifier.interfaces import ISectionBlueprint, ISection
from collective.transmogrifier.tests import tearDown
from collective.transmogrifier.sections.tests import sectionsSetUp
from collective.transmogrifier.sections.tests import SampleSource
from Products.Five import zcml

# Doctest support

ctSectionsSetup = sectionsSetUp
def sectionsSetUp(test):
    ctSectionsSetup(test)
    import plone.app.transmogrifier
    zcml.load_config('configure.zcml', plone.app.transmogrifier)

def portalTransformsSetUp(test):
    sectionsSetUp(test)
    
    class MockPortalTransforms(object):
        def __call__(self, transform, data):
            return 'Transformed %r using the %s transform' % (data, transform)
        def convertToData(self, target, data, mimetype=None):
            if mimetype is not None:
                return 'Transformed %r from %s to %s' % (
                    data, mimetype, target)
            else:
                return 'Transformed %r to %s' % (data, target)
    test.globs['plone'].portal_transforms = MockPortalTransforms()

def aTSchemaUpdaterSetUp(test):
    sectionsSetUp(test)
    
    from plone.app.transmogrifier.interfaces import IBaseObject
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
            if path.endswith('/notatcontent'):
                return object()
            self._last_path = path
            return self
        
        _last_field = None
        def getField(self, name):
            if name.startswith('field'):
                self._last_field = name
                return self
        
        def get(self, ob):
            if self._last_field.endswith('notchanged'):
                return 'nochange'
            if self._last_field.endswith('unicode'):
                return u'\xe5'.encode('utf8')
        
        updated = ()
        def set(self, ob, val):
            self.updated += ((self._last_path, self._last_field, val),)
        
        def checkCreationFlag(self):
            return len(self.updated) % 2
        
        def unmarkCreationFlag(self):
            pass
        
        def at_post_create_script(self):
            pass
        
        def at_post_edit_script(self):
            pass
    
    test.globs['plone'] = MockPortal()
    test.globs['transmogrifier'].context = test.globs['plone']
    
    class SchemaSource(SampleSource):
        classProvides(ISectionBlueprint)
        implements(ISection)
        
        def __init__(self, *args, **kw):
            super(SchemaSource, self).__init__(*args, **kw)
            self.sample = (
                dict(_path='/spam/eggs/foo', fieldone='one value', 
                     fieldtwo=2, nosuchfield='ignored',
                     fieldnotchanged='nochange', fieldunicode=u'\xe5',),
                dict(_path='not/existing/bar', fieldone='one value',
                     title='Should not be updated, not an existing path'),
                dict(fieldone='one value',
                     title='Should not be updated, no path'),
                dict(_path='/spam/eggs/notatcontent', fieldtwo=2,
                     title='Should not be updated, not an AT base object'),
            )
    provideUtility(SchemaSource,
        name=u'plone.app.transmogrifier.tests.schemasource')

def workflowUpdaterSetUp(test):
    sectionsSetUp(test)
    
    from Products.CMFCore.WorkflowCore import WorkflowException
    
    class MockPortal(object):
        _last_path = None
        def unrestrictedTraverse(self, path, default):
            if path[0] == '/':
                return default # path is absolute
            if isinstance(path, unicode):
                return default
            if path == 'not/existing/bar':
                return default
            self._last_path = path
            return self
        
        @property
        def portal_workflow(self):
            return self
        
        updated = ()
        def doActionFor(self, ob, action):
            assert ob == self
            if action == 'nonsuch':
                raise WorkflowException('Test exception')
            self.updated += ((self._last_path, action),)

    test.globs['plone'] = MockPortal()
    test.globs['transmogrifier'].context = test.globs['plone']

    class WorkflowSource(SampleSource):
        classProvides(ISectionBlueprint)
        implements(ISection)

        def __init__(self, *args, **kw):
            super(WorkflowSource, self).__init__(*args, **kw)
            self.sample = (
                dict(_path='/spam/eggs/foo', _transitions='spam'),
                dict(_path='/spam/eggs/baz', _transitions=('spam', 'eggs')),
                dict(_path='not/existing/bar', _transitions=('spam', 'eggs'),
                     title='Should not be updated, not an existing path'),
                dict(_path='spam/eggs/incomplete',
                     title='Should not be updated, no transitions'),
                dict(_path='/spam/eggs/nosuchtransition', 
                     _transitions=('nonsuch',),
                     title='Should not be updated, no such transition'),
            )
    provideUtility(WorkflowSource,
        name=u'plone.app.transmogrifier.tests.workflowsource')


def browserDefaultSetUp(test):
    sectionsSetUp(test)

    from plone.app.transmogrifier.interfaces import ISelectableBrowserDefault
    class MockPortal(object):
        implements(ISelectableBrowserDefault)

        _last_path = None
        def unrestrictedTraverse(self, path, default):
            if path[0] == '/':
                return default # path is absolute
            if isinstance(path, unicode):
                return default
            if path == 'not/existing/bar':
                return default
            self._last_path = path
            return self

        updated = ()
        def setLayout(self, layout):
            self.updated += ((self._last_path, 'layout', layout),)

        def setDefaultPage(self, defaultpage):
            self.updated += ((self._last_path, 'defaultpage', defaultpage),)

    test.globs['plone'] = MockPortal()
    test.globs['transmogrifier'].context = test.globs['plone']

    class BrowserDefaultSource(SampleSource):
        classProvides(ISectionBlueprint)
        implements(ISection)

        def __init__(self, *args, **kw):
            super(BrowserDefaultSource, self).__init__(*args, **kw)
            self.sample = (
                dict(_path='/spam/eggs/foo', _layout='spam'),
                dict(_path='/spam/eggs/bar', _defaultpage='eggs'),
                dict(_path='/spam/eggs/baz', _layout='spam', _defaultpage='eggs'),
                dict(_path='not/existing/bar', _layout='spam',
                     title='Should not be updated, not an existing path'),
                dict(_path='spam/eggs/incomplete',
                     title='Should not be updated, no layout or defaultpage'),
            )
    provideUtility(BrowserDefaultSource,
        name=u'plone.app.transmogrifier.tests.browserdefaultsource')


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'portaltransforms.txt',
            setUp=portalTransformsSetUp, tearDown=tearDown),
        doctest.DocFileSuite(
            'atschemaupdater.txt',
            setUp=aTSchemaUpdaterSetUp, tearDown=tearDown),
        doctest.DocFileSuite(
            'workflowupdater.txt',
            setUp=workflowUpdaterSetUp, tearDown=tearDown),
        doctest.DocFileSuite(
            'browserdefault.txt',
            setUp=browserDefaultSetUp, tearDown=tearDown),
    ))
