from zope.interface import classProvides, implements
from zope.component import queryAdapter

from collective.transmogrifier.interfaces import ISection, ISectionBlueprint
from collective.transmogrifier.utils import defaultMatcher

from quintagroup.transmogrifier.simpleblog2quills.interfaces import \
    IItemManipulator, IExportItemManipulator, IImportItemManipulator

class ItemManipulatorSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context

        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')

        # 'type' options specifies adapter interface
        type_ = options.get('type', 'general')
        if type_ == 'general':
            self.interface = IItemManipulator
        elif type_ == 'export':
            self.interface = IExportItemManipulator
        elif type_ == 'import':
            self.interface = IImportItemManipulator
        else:
            self.interface = None

    def __iter__(self):
        for item in self.previous:
            pathkey = self.pathkey(*item.keys())[0]

            if not (pathkey and self.interface is not None):
                yield item; continue

            path = item[pathkey]
            obj = self.context.unrestrictedTraverse(path, None)
            if obj is None:         # path doesn't exist
                yield item; continue

            adapter = queryAdapter(obj, self.interface, name='')
            if adapter:
                item = adapter(item, path=pathkey)

            yield item
