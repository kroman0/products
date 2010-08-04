"""
    Archetypes Marshall namespace but which can safely handle
    Control Characters for you
"""

from Products.Archetypes.interfaces.base import IBaseUnit

from Products.Marshall import config
from Products.Marshall.handlers.atxml import XmlNamespace
from Products.Marshall.handlers.atxml import SchemaAttribute
from Products.Marshall.handlers.atxml import getRegisteredNamespaces
from Products.Marshall.exceptions import MarshallingException
from Products.Marshall import utils

from Products.Marshall.namespaces import atns as base

from quintagroup.transmogrifier.namespaces.util import has_ctrlchars

_marker = ()

class ATAttribute(base.ATAttribute):

    def serialize(self, dom, parent_node, instance, options={}):

        def getPreparedValue(value):
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif IBaseUnit.isImplementedBy(value):
                value = value.getRaw(encoding='utf-8')
            else:
                value = str(value)
            return value


        def addNode(node, value, nspref):
            if is_ref:
                if config.HANDLE_REFS:
                    ref_node = dom.createElementNS(nspref, 'reference')
                    uid_node = dom.createElementNS(nspref, 'uid')
                    value = response.createTextNode(value)
                    uid_node.append(value)
                    ref_node.append(uid_node)
                    node.append(ref_node)

            elif isinstance(value, str) and has_ctrlchars(value):
                value = value.encode('base64')
                attr = dom.createAttributeNS(nspref, 'transfer_encoding')
                attr.value = 'base64'
                node.setAttributeNode(attr)
                value_node = dom.createCDATASection(value)
                node.appendChild(value_node)
            else:
                value_node = dom.createTextNode(value)
                node.appendChild(value_node)

        values = self.get(instance)
        if not values:
            return

        is_ref = self.isReference(instance)
        
        for value in values:
            node = dom.createElementNS(self.namespace.xmlns, "field")
            name_attr = dom.createAttribute("name")
            name_attr.value = self.name
            node.setAttributeNode(name_attr)
            
            # try to get 'utf-8' encoded string
            items = getattr(value, 'items', _marker)
            if items is not _marker and callable(items):
                # Map field
                # set type attribute for the field
                type_attr = dom.createAttribute("type")
                type_attr.value = "dict"
                node.setAttributeNode(type_attr)
                for k, v in items():
                    # create item node with key attribute
                    good_key = getPreparedValue(k)
                    item_node = dom.createElementNS(self.namespace.xmlns, "item")
                    key_attr = dom.createAttribute("key")
                    key_attr.value = good_key
                    item_node.setAttributeNode(key_attr)
                    # prepare value for the item
                    good_value = getPreparedValue(v)
                    addNode(item_node, good_value, self.namespace.xmlns)
                    item_node.normalize()
                    node.appendChild(item_node)
            else:
                # Common field
                value = getPreparedValue(value)
                addNode(node, value, self.namespace.xmlns)
        
            node.normalize()
            parent_node.appendChild(node)

        return True

    def processXmlValue(self, context, value):
        def getValue(node, value):
            if value is None:
                return
            value = value.strip()
            if not value:
                return
            # decode node value if needed
            te = node.get('transfer_encoding', None)
            if te is not None:
                value = value.decode(te)
            return value
            
        # Get value type
        vtype = context.node.attrib.get('type', None)
        if vtype=='dict':
            # process dictionary type
            d = {}
            for item in context.node:
                k = item.get("key", None)
                v = getValue(item, item.text)
                if k and v:
                    d[k] = v
            value = d
        else:
            # Common field
            value = getValue(context.node, value)

        if not value:
            return

        data = context.getDataFor(self.namespace.xmlns)
        if data.has_key(self.name):
            svalues = data[self.name]
            if not isinstance(svalues, list):
                data[self.name] = svalues = [svalues]
            svalues.append(value)
            return
        else:
            data[self.name] = value

class Archetypes(base.Archetypes):

    def getAttributeByName(self, schema_name, context=None):
        if context is not None and schema_name not in self.at_fields:
            if not context.instance.Schema().has_key(schema_name):
                return
                raise AssertionError, \
                      "invalid attribute %s"%(schema_name)
        
        if schema_name in self.at_fields:
            return self.at_fields[schema_name]

        attribute = ATAttribute(schema_name)
        attribute.setNamespace(self)
        
        return attribute
