import os.path

from zope.interface import classProvides, implements

from collective.transmogrifier.interfaces import ISectionBlueprint, ISection

class Source(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.source = options.get('source', '').strip()
        self.allow_empty = options.get('allow-empty-items', '').strip() == 'yes' and True or False
        items_source = options.get('items', '').strip()
        self.items = []
        for line in items_source.splitlines():
            self.items.append([i.strip() for i in line.split(';')])

    def __iter__(self):
        for item in self.previous:
            yield item

        for path, type_, fname in self.items:
            if not fname.startswith('/'):
                fname = os.path.join(os.path.dirname(__file__), fname)
            try:
                fp = file(fname)
                data = fp.read()
                fp.close()
            except IOError, e:
                if self.allow_empty:
                    yield dict(_type=type_, _path=path)
                continue

            item = dict(
                _type=type_,
                _path=path,
                _files={
                    self.source: {'data': data}
                }
            )
            yield item
