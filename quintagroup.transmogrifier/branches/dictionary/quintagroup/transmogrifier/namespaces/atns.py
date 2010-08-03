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



#######################################
#         Setup logging system        #
#######################################
import logging
DEFAULT_LOG = "/tmp/quintagroup.transmogrifier.log"
FORMAT = "[%(asctime)s]: %(message)s"
#FORMAT = "[%H:%M:%S]: %(message)s"
def createHandler(hndlr_cls, level, *args, **kwargs):
    hndlr = hndlr_cls(*args, **kwargs)
    hndlr.setLevel(level)
    hndlr.setFormatter(logging.Formatter(FORMAT, datefmt="%H:%M:%S"))
    return hndlr

# Very IMPORTANT create logger as logging.Logger NOT logging.getLogger !!!
logger = logging.Logger("Quintagroup Transmogrifier", logging.NOTSET)
logger.addHandler(createHandler(
        logging.FileHandler, logging.DEBUG, DEFAULT_LOG))

#######################################

_marker = ()


class ATAttribute(base.ATAttribute):

    def serialize(self, dom, parent_node, instance, options={}):
        
        values = self.get(instance)
        if not values:
            return

        # if self.name in ['payablesMap', 'fieldMap']:
        #     import ipdb;ipdb.set_trace()

        is_ref = self.isReference(instance)
        
        for value in values:
            node = dom.createElementNS(self.namespace.xmlns, "field")
            name_attr = dom.createAttribute("name")
            name_attr.value = self.name
            node.setAttributeNode(name_attr)
            
            # try to get 'utf-8' encoded string
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif IBaseUnit.isImplementedBy(value):
                value = value.getRaw(encoding='utf-8')
            else:
                value = str(value)

            if is_ref:
                if config.HANDLE_REFS:
                    ref_node = dom.createElementNS(self.namespace.xmlns,
                                                    'reference')
                    uid_node = dom.createElementNS(self.namespace.xmlns,
                                                    'uid')
                    value = response.createTextNode(value)
                    uid_node.append(value)
                    ref_node.append(uid_node)
                    node.append(ref_node)
            elif isinstance(value, str) and has_ctrlchars(value):
                value = value.encode('base64')
                attr = dom.createAttributeNS(self.namespace.xmlns,
                                             'transfer_encoding')
                attr.value = 'base64'
                node.setAttributeNode(attr)
                value_node = dom.createCDATASection(value)
                node.appendChild(value_node)
            else:
                items = getattr(value, 'items', _marker)
                if items is not _marker and callable(items):
                    type_attr = dom.createAttribute("type")
                    type_attr.value = "dict"
                    node.setAttributeNode( type_attr )
                value_node = dom.createTextNode(value)
                node.appendChild(value_node)
        
            node.normalize()
            parent_node.appendChild(node)

        return True

    def processXmlValue(self, context, value):
        if value is None:
            return

        value = value.strip()
        if not value:
            return

        # decode node value if needed
        te = context.node.get('transfer_encoding', None)
        if te is not None:
            value = value.decode(te)
        # process dictionary type
        vtype = context.node.attrib.get('type', None)
        if vtype and vtype=='dict':
            try:
                s = value.strip("{}\t\n")
                # value = dict([map(lambda x:x.strip(" '\""), item.split("': '")) \
                #              for item in s.split("', '")])
                value = dict([map(lambda x:x.strip(" '\""), item.split(": ")) \
                             for item in s.split(", ")])
            except:
                #import ipdb;ipdb.set_trace()
                logger.error("Error on processing '%s' dict type field,\n"\
                    " for object: '%s'\n  " \
                    " for the following data: '%s'" % (str(context.instance.id),
                     context.instance.absolute_url(), str(value)))


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
