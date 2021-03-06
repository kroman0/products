import os.path
from xml.dom import minidom

from zope.interface import classProvides, implements
from zope.annotation.interfaces import IAnnotations

from collective.transmogrifier.interfaces import ISection, ISectionBlueprint
from collective.transmogrifier.utils import defaultMatcher

from quintagroup.transmogrifier.logger import VALIDATIONKEY

class ManifestExporterSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context

        self.entrieskey = defaultMatcher(options, 'entries-key', name, 'entries')
        self.fileskey = options.get('files-key', '_files').strip()

        self.doc = minidom.Document()

    def __iter__(self):
        for item in self.previous:
            entrieskey = self.entrieskey(*item.keys())[0]
            if not entrieskey:
                yield item; continue

            manifest = self.createManifest(item[entrieskey])

            if manifest:
                files = item.setdefault('_files', {})
                item[self.fileskey]['manifest'] = {
                    'name': '.objects.xml',
                    'data': manifest,
                }

            yield item

    def createManifest(self, entries):
        if not entries:
            return None

        doc = self.doc
        root = doc.createElement('manifest')

        for obj_id, obj_type in entries:
            # create record
            record = doc.createElement('record')

            # set type attribute
            attr = doc.createAttribute('type')
            attr.value = obj_type
            record.setAttributeNode(attr)

            # add object id
            text = doc.createTextNode(obj_id)
            record.appendChild(text)

            root.appendChild(record)

        doc.appendChild(root)

        try:
            data = doc.toprettyxml(indent='  ', encoding='utf-8')
        except UnicodeDecodeError, e:
            # all comments are strings encoded in 'utf-8' and they will properly
            # saved in xml file, but if we explicitly give 'utf-8' encoding
            # UnicodeDecodeError will be raised when they have non-ascii chars
            data = doc.toprettyxml(indent='  ')

        doc.unlink()
        return data

class ManifestImporterSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context

        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')
        self.fileskey = defaultMatcher(options, 'files-key', name, 'files')
        self.typekey = options.get('type-key', '_type').strip()
        self.enable_source_behaviour = options.get('enable-source-behaviour', 'true') == 'true' and True or False

        # communication with logger
        self.anno = IAnnotations(transmogrifier)
        self.storage = self.anno.setdefault(VALIDATIONKEY, [])

        # we need this dictionary to store manifest data, because reader section
        # uses recursion when walking through content folders
        self.manifests = {}

    def __iter__(self):
        for item in self.previous:
            pathkey = self.pathkey(*item.keys())[0]
            fileskey = self.fileskey(*item.keys())[0]

            # skip items without path
            if not pathkey: continue

            path  = item[pathkey]

            if path != '':
                parent, item_id = os.path.split(path)
                manifest = self.manifests.get(parent, {})

                # skip that are not listed in their parent's manifest
                if item_id not in manifest: continue

                item[self.typekey] = manifest.pop(item_id)
                # remove empty manifest dict
                if not manifest:
                    del self.manifests[parent]

            # this item is folderish - parse manifest
            if fileskey and 'manifest' in item[fileskey]:
                self.extractManifest(path, item[fileskey]['manifest']['data'])

            yield item

        # now we yield items that were defined in manifests but not generated by
        # previous sections - it is possible
        if self.manifests and self.enable_source_behaviour:
            containers = self.manifests.keys()
            containers.sort()
            for i in containers:
                manifest = self.manifests[i]
                ids = manifest.keys()
                ids.sort()
                for id_ in ids:
                    if i == '':
                        path = id_
                    else:
                        path = '/'.join([i, id_])
                    self.storage.append(path)
                    yield {pathkey: path, self.typekey: manifest[id_]}

        # cleanup
        if VALIDATIONKEY in self.anno:
            del self.anno[VALIDATIONKEY]

    def extractManifest(self, path, data):
        doc = minidom.parseString(data)
        objects = {}
        for record in doc.getElementsByTagName('record'):
            type_ = str(record.getAttribute('type'))
            object_id = str(record.firstChild.nodeValue.strip())
            objects[object_id] = type_
        self.manifests[path] = objects
