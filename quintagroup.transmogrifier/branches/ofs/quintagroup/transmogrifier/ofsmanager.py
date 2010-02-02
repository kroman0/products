import traceback
from xml.dom import minidom

from zope.interface import classProvides, implements

from collective.transmogrifier.interfaces import ISection, ISectionBlueprint
from collective.transmogrifier.utils import defaultMatcher, Condition

class OFSExporterSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context

        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')
        self.fileskey = options.get('files-key', '_files').strip()

        self.doc = minidom.Document()
        self.condition = Condition(options.get('condition', 'python:True'),
                                   transmogrifier, name, options)

    def __iter__(self):
        for item in self.previous:
            pathkey = self.pathkey(*item.keys())[0]

            if not pathkey:
                yield item; continue

            path = item[pathkey]
            files = item.setdefault(self.fileskey, {})
            obj = self.context.unrestrictedTraverse(path, None)
            if obj is None:         # path doesn't exist
                yield item; continue

            if obj.meta_type in ["File", "Image"]:
                name = getattr(obj, '__name__', obj.id())
                data = getattr(obj, 'data', '')
                fields = {'__name__': name,
                          'title': getattr(obj, 'title', name),
                          'precondition': getattr(obj, 'precondition', ''),
                          'size': getattr(obj, 'get_size', lambda o:0)(),
                          'content_type': getattr(obj, 'content_type', ''),
                          }

                if obj.meta_type == "Image":
                    fields['width'] = getattr(obj, 'width', 0)
                    fields['height'] = getattr(obj, 'height', 0)

                if not self.condition(item, context=obj,
                                      fprop_info=fields):
                    continue

                files['file-properties'] = {
                    'name': '.file-properties.xml',
                    'data': self.createManifest(fields),
                    }

                if len(data) > 0:
                    files[fields['__name__']] = {
                        'name': name,
                        'data': data,
                        'content_type': fields['content_type'],
                        }

            yield item


    def createManifest(self, props):
        doc = self.doc

        root = doc.createElement('manifest')
        for name, val in props.items():
            # create field node
            prop = doc.createElement('prop')

            # set id attribute
            attr_id = doc.createAttribute('id')
            attr_id.value = name
            prop.setAttributeNode(attr_id)

            # add value
            v = doc.createTextNode(str(val))
            prop.appendChild(v)

            root.appendChild(prop)

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


class OFSImporterSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context

        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')
        self.fileskey = defaultMatcher(options, 'files-key', name, 'files')
        self.contextkey = defaultMatcher(options, 'context-key', name, 'import_context')

        self.condition = Condition(options.get('condition', 'python:True'),
                                   transmogrifier, name, options)

    def __iter__(self):
        for item in self.previous:
            pathkey = self.pathkey(*item.keys())[0]
            fileskey = self.fileskey(*item.keys())[0]

            if not (pathkey and fileskey):
                yield item; continue
            if 'file-properties' not in item[fileskey]:
                yield item; continue

            path = item[pathkey]
            obj = self.context.unrestrictedTraverse(path, None)
            if obj is None:         # path doesn't exist
                yield item; continue

            if obj.meta_type in ["File", "Image"]:
                try:
                    manifest = item[fileskey]['file-properties']['data']
                    prop_info = self.parseManifest(manifest)
                    # Update file/image properties
                    if not self.condition(item, context=obj,
                                          fprop_info=prop_info):
                        continue
                    for prop_id, prop_val in prop_info.items():
                        setattr(obj, prop_id, prop_val)

                    # Add data for file/image
                    name = prop_info.get('__name__', None)
                    if name is None:
                        continue
                    data = item[fileskey].get(name, None)
                    if data is None:
                        continue
                    obj.data = data['data']
                    
                except Exception, e:
                    print "Exception in ofsimporter section:"
                    print '-'*60
                    traceback.print_exc()
                    print '-'*60

            yield item

    def parseManifest(self, manifest):
        doc = minidom.parseString(manifest)
        props = {}
        for prop in doc.getElementsByTagName('prop'):
            prop_id = str(prop.getAttribute('id'))
            if not prop_id:
                continue
            props[prop_id] = str(prop.firstChild.nodeValue.strip())

        return props
