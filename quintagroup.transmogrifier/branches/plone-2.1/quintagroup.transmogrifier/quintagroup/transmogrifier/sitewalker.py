from zope.interface import classProvides, implements

from collective.transmogrifier.interfaces import ISection, ISectionBlueprint

from collective.transmogrifier.interfaces import IFolderish

from interfaces import IBaseFolder

class SiteWalkerSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context

        excluded_types = options.get('excluded-types', '')
        self.excluded_types = filter(None, [i.strip() for i in excluded_types.splitlines()])

    def getContained(self, obj):
        contained = [(k, v.getPortalTypeName()) for k, v in obj.contentItems()]
        contained = [i for i in contained if i[1] not in self.excluded_types]
        return tuple(contained)

    def walk(self, obj):
        if IFolderish.providedBy(obj) or IBaseFolder.providedBy(obj):
            contained = self.getContained(obj)
            yield obj, contained
            for v in obj.contentValues():
                for x in self.walk(v):
                    yield x
        else:
            yield obj, ()

    def __iter__(self):
        for item in self.previous:
            yield item

        for obj, contained in self.walk(self.context):
            type_ = obj.getPortalTypeName()
            if type_ in self.excluded_types:
                continue
            item = {
                '_path': '/'.join(obj.getPhysicalPath()[2:]),
                '_type': type_,
            }
            if contained:
                item['_entries'] = contained
            yield item
