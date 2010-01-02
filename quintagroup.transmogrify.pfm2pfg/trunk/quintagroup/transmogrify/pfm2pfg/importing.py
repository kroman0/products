import logging
import os.path
from xml.dom import minidom
from DateTime import DateTime

from zope.interface import implements, Interface
from zope.component import getUtility

from ZODB.POSException import ConflictError
from Acquisition import aq_inner, aq_parent

from Products.Marshall.registry import getComponent
from Products.Marshall.config import AT_NS
from Products.CMFPlone.utils import _createObjectByType

from quintagroup.transmogrifier.interfaces import IImportDataCorrector
from quintagroup.transmogrifier.adapters.importing import ReferenceImporter
from quintagroup.transmogrifier.xslt import XSLTSection

BOOL_FIELD_PROPS = ['enabled', 'required', 'hidden']

FIELD_MAP = {
            'StringField'   : 'FormStringField',
            'EmailField'    : ('FormStringField', {'fgStringValidator': 'isEmail'}),
            'LinkField'     : ('FormStringField', {'fgStringValidator': 'isURL'}),
            'PatternField'  : 'FormStringField',

            'TextAreaField' : 'FormTextField',
            'RawTextAreaField': 'FormTextField',

            'PasswordField' : 'FormPasswordField',
            'LabelField'    : 'FormRichLabelField', #FormLabelField

            'IntegerField'  : 'FormIntegerField',
            'FloatField'    : 'FormFixedPointField',

            'DateTimeField' : 'FormDateField',
            'FileField'     : 'FormFileField',

            'LinesField'    : 'FormLinesField',

            'CheckBoxField' : 'FormBooleanField',
            'ListField'     : ('FormSelectionField', {'fgFormat': 'select'}),
            'RadioField'    : ('FormSelectionField', {'fgFormat': 'radio'}),
            'MultiListField': ('FormMultiSelectionField', {'fgFormat': 'select'}),
            'MultiCheckBoxField':('FormMultiSelectionField', {'fgFormat': 'checkbox'}),
            }

class IXMLDemarshaller(Interface):
    """
    """
    def demarshall(obj, data):
        """
        """

class FormFolderImporter(ReferenceImporter):
    """ Demarshaller of PloneFormGen's FormFolder content type.
    """
    implements(IImportDataCorrector)

    def __init__(self, context, transmogrifier):
        self.context = context
        self.demarshaller = getComponent("atxml")
        self.auto_added_fgfields = ['replyto', 'topic', 'comments']
        self.date_fields = {}

    def __call__(self, data):
        data = super(FormFolderImporter, self).__call__(data)
        xml = data['data']
        data['data'] = self.transformWithMinidom(xml)

        # update FormMailerAdapter and FormThanksPage objects
        cleaned_xml = self.updateMailer(xml)

        self.updateResponsePage(cleaned_xml)

        self.updateFormFields(xml)

        return data

    def transformWithMinidom(self, xml):
        """ Do some extra transformations on xml document (that can be done by XSLT).
        """
        doc = minidom.parseString(xml)
        root = doc.documentElement

        # get 'modification_date' and 'creation_date' for next usage when creating fields
        for i in root.getElementsByTagName('xmp:CreateDate'):
            self.date_fields['creation_date'] = i.firstChild.nodeValue.strip()
        for i in root.getElementsByTagName('xmp:ModifyDate'):
            self.date_fields['modification_date'] = i.firstChild.nodeValue.strip()

        # xxx: update button labels (those elements are now skiped by xslt)
        # PFM has only one field 'form_buttons', but PFG has two: 'submitLabel', 'resetLabel' and
        # field 'useCancelButton'

        # add element for setting of 'thanksPage' field to 'thank-you' FormThanksPage
        elem = doc.createElementNS(AT_NS, "field")
        name_attr = doc.createAttribute("name")
        name_attr.value = 'thanksPage'
        elem.setAttributeNode(name_attr)
        value = doc.createTextNode('thank-you')
        elem.appendChild(value)
        root.appendChild(elem)

        # update 'thanksPageOverride' field
        elem = [i for i in doc.getElementsByTagName('field') if i.getAttribute('name') == 'thanksPageOverride']
        if elem:
            elem = elem[0]
            old_text = elem.firstChild
            new_text = doc.createTextNode('redirect_to:' + old_text.nodeValue.strip())
            elem.removeChild(old_text)
            elem.appendChild(new_text)

        # xxx: update 'afterValidationOverride' field
        # 'afterValidationOverride' is TALES expression, but PFM's 'cpyaction' is name 
        # of controller python script
        elem = [i for i in doc.getElementsByTagName('field') 
                if i.getAttribute('name') == 'afterValidationOverride']
        if elem:
            elem = elem[0]
            old_text = elem.firstChild
            new_text = doc.createTextNode('string:' + old_text.nodeValue.strip())
            elem.removeChild(old_text)
            elem.appendChild(new_text)

        # xxx: update 'onDisplayOverride' field (this element is now skiped by xslt)
        # 'onDisplayOverride' is TALES expression, but PFM's 'before_script' is python script
        # in 'scripts' subfolder

        return doc.toxml('utf-8')

    def updateMailer(self, xml):
        mailer = self.context['mailer']
        transformed = self.transformWithXSLT(xml, 'FormMailerAdapter')
        self.demarshaller.demarshall(mailer, transformed)
        mailer.indexObject()
        return transformed

    def updateResponsePage(self, xml):
        page = self.context['thank-you']
        transformed = self.transformWithXSLT(xml, 'FormThanksPage')
        self.demarshaller.demarshall(page, transformed)
        # override default value of description field
        page.getField('description').getMutator(page)('')
        page.indexObject()
        return transformed

    def transformWithXSLT(self, xml, to):
        """ Apply XSLT transformations using XSLT transmogrifier section.
        """
        item = dict(
            _from='PloneFormMailer',
            _to=to,
            _files=dict(
                marshall=dict(
                    name='.marshall.xml',
                    data=xml
                )
            )
        )
        section = XSLTSection(object(), 'xslt', {'blueprint': ''}, iter((item,)))
        for i in section: pass
        return item['_files']['marshall']['data']

    def updateFormFields(self, data):
        """ Walk trough xml tree and create fields in FormFolder.
        """
        # delete fields that were added on FormFolder creation
        for oid in [i for i in self.auto_added_fgfields if i in self.context]:
            self.context._delObject(oid)

        doc = minidom.parseString(data)
        root = doc.documentElement
        form_element = root.getElementsByTagName('form')
        if not form_element:
            return
        groups = form_element[0].getElementsByTagName('group')
        for group in groups:
            group_title = group.getElementsByTagName('title')[0]
            group_title = str(group_title.firstChild.nodeValue).strip()
            if group_title == 'Default':
                for field in group.getElementsByTagName('field'):
                    field_id = str(field.getElementsByTagName('id')[0].firstChild.nodeValue).strip()
                    field_type = str(field.getElementsByTagName('type')[0].firstChild.nodeValue).strip()
                    self.createField(field_type, field_id, field, self.context)
            else:
                fieldset = self.createFieldset(group_title)
                if not fieldset:
                    return
                for field in group.getElementsByTagName('field'):
                    field_id = str(field.getElementsByTagName('id')[0].firstChild.nodeValue).strip()
                    field_type = str(field.getElementsByTagName('type')[0].firstChild.nodeValue).strip()
                    self.createField(field_type, field_id, field, fieldset)

    def createField(self, type_name, field_id, field_node, context=None):
        """ Created formfield and update it from field_node's xml tree.

            Use demarshalling adapter.
        """
        if FIELD_MAP.get(type_name) is None:
            return

        if isinstance(FIELD_MAP[type_name], tuple):
            type_name, options = FIELD_MAP[type_name]
        else:
            type_name, options = FIELD_MAP[type_name], {}
        # update options with 'creation_date' and 'modification_date', that are
        # the same as in FormFolder (dates on fields must be the same)
        options.update(self.date_fields)

        if field_id not in context.contentIds():
            try:
                field = _createObjectByType(type_name, context, field_id)
            except ConflictError:
                raise
            except:
                return
        else:
            field = context._getOb(field_id)

        try:
            IXMLDemarshaller(field).demarshall(field_node, **options)
        except ConflictError:
            raise

    def createFieldset(self, title):
        """ Create FieldsetFolder with id=title
        """
        if title not in self.context.contentIds():
            try:
                fieldset = _createObjectByType('FieldsetFolder', self.context, title)
            except ConflictError:
                raise
            except:
                return
        else:
            fieldset = self.context._getOb(title)
        fieldset.Schema()['title'].getMutator(fieldset)(title)

        return fieldset

class BaseFieldDemarshaller(object):
    """ Base class for demarshallers of PloneFormGen's fields from PloneFormMailer fields.
    """
    implements(IXMLDemarshaller)

    def __init__(self, context):
        self.context = context

    def demarshall(self, node, **kw):
        self.extractData(node)
        # update data dictionary form keyword arguments
        for k, v in kw.items():
            self.data[k] = v
        # call special hook for changing data
        self.modifyData()

        # update instance
        schema = self.context.Schema()
        for fname, value in self.data.items():
            if not schema.has_key(fname):
                continue
            mutator = schema[fname].getMutator(self.context)
            if not mutator:
                continue
            mutator(value)

        self.context.indexObject()

    def extractData(self, node):
        tree = XMLObject()
        elementToObject(tree, node)
        simplify_single_entries(tree)

        data = {}
        values = tree.first.field.first.values
        for name in values.getElementNames():
            value = getattr(values.first, name)
            if value.attributes.get('type') == 'float':
                data[name] = float(value.text)
            elif value.attributes.get('type') == 'int':
                data[name] = int(value.text)
                # boolean property is exported as int, fix that
                if name in BOOL_FIELD_PROPS:
                    data[name] = bool(data[name])
            elif value.attributes.get('type') == 'list':
                # XXX bare eval here (this may be a security leak ?)
                data[name] = eval(str(value.text))
            elif value.attributes.get('type') == 'datetime':
                data[name] = DateTime(value.text)
            else:
                data[name] = str(value.text)

        # get tales expressions
        tales = tree.first.field.first.tales
        for name in tales.getElementNames():
            value = getattr(tales.first, name)
            data["tales:"+name] = str(value.text)

        self.data = data

    def modifyData(self):
        pass

    def renameEntry(self, old, new):
        if self.data.has_key(old):
            self.data[new] = self.data.pop(old)

    def entryIsDigit(self, key):
        """ Formulator exports empty fields in xml as empty elements without
            'type' attribute. That's is why we get in data dictionary for 
            integer fields values that are empty strings. This method is 
            used to check whether integer field has integer value.
        """
        if key in self.data and isinstance(self.data[key], int):
            return True
        else:
            return False

class StringFieldDemarshaller(BaseFieldDemarshaller):
    """ Demarshaller of StringField and other fields of this kind.
    """

    def modifyData(self):
        self.renameEntry('default', 'fgDefault')
        if self.entryIsDigit('display_maxwidth'):
            self.renameEntry('display_maxwidth', 'fgmaxlength')
        if self.entryIsDigit('display_width'):
            self.renameEntry('display_width', 'fgsize')

class TextFieldDemarshaller(BaseFieldDemarshaller):
    """ Demarshaller of TextField.
    """

    def modifyData(self):
        self.renameEntry('default', 'fgDefault')
        if self.entryIsDigit('max_length'):
            self.renameEntry('max_length', 'fgmaxlength')
        if self.entryIsDigit('height'):
            self.renameEntry('height', 'fgRows')

class LabelFieldDemarshaller(BaseFieldDemarshaller):
    """ Demarshaller of  LabelField.
    """

    def modifyData(self):
        self.renameEntry('default', 'fgDefault')

class IntegerFieldDemarshaller(BaseFieldDemarshaller):
    """ Demarshaller of IntegerField.
    """

    def modifyData(self):
        self.renameEntry('default', 'fgDefault')
        if self.entryIsDigit('display_maxwidth'):
            self.renameEntry('display_maxwidth', 'fgmaxlength')
        if self.entryIsDigit('display_width'):
            self.renameEntry('display_width', 'fgsize')
        if self.entryIsDigit('start'):
            self.renameEntry('start', 'minval')
        if self.entryIsDigit('end'):
            self.renameEntry('end', 'maxval')

class DateTimeFieldDemarshaller(BaseFieldDemarshaller):
    """ Demarshaller of DateTimeField.
    """

    def modifyData(self):
        if 'default' in self.data:
            # convert from DateTime object to string
            self.data['default'] = str(self.data['default'])
            self.renameEntry('default', 'fgDefault')
        # date_only is boolean flag
        self.data['fgShowHM'] = not bool(self.data['date_only'])
        if 'start_datetime' in self.data:
            self.data['start_datetime'] = self.data['start_datetime'].year()
            self.renameEntry('start_datetime', 'fgStartingYear')
        if 'end_datetime' in self.data:
            self.data['end_datetime'] = self.data['end_datetime'].year()
            self.renameEntry('end_datetime', 'fgEndingYear')

class LinesFieldDemarshaller(BaseFieldDemarshaller):
    """ Demarshaller of LinesField.
    """

    def modifyData(self):
        self.renameEntry('default', 'fgDefault')
        if self.entryIsDigit('height'):
            self.renameEntry('height', 'fgRows')

class BooleanFieldDemarshaller(BaseFieldDemarshaller):
    """ Demarshaller of BooleanField.
    """

    def modifyData(self):
        self.data['default'] = bool(self.data['default'])
        self.renameEntry('default', 'fgDefault')


class SelectionFieldDemarshaller(BaseFieldDemarshaller):
    """ Demarshaller of SelectionField.
    """

    def modifyData(self):
        self.renameEntry('default', 'fgDefault')
        l = []
        for i in self.data['items']:
            i = list(i)
            i.reverse()
            l.append(i)
        self.data['items'] = ['|'.join(i) for i in l]
        self.renameEntry('items', 'fgVocabulary')

class MultiSelectFieldDemarshaller(SelectionFieldDemarshaller):
    """ Demarshaller of MultiSelectField.
    """

    def modifyData(self):
        super(MultiSelectFieldDemarshaller, self).modifyData()
        if self.entryIsDigit('size'):
            self.renameEntry('size', 'fgRows')


# next code was stolen from Formulator product
from xml.dom.minidom import parse, parseString, Node

# an extremely simple system for loading in XML into objects

class Object:
    pass

class XMLObject:
    def __init__(self):
        self.elements = Object()
        self.first = Object()
        self.attributes = {}
        self.text = ''

    def getElementNames(self):
        return [element for element in dir(self.elements)
                if not element.startswith('__')]

    def getAttributes(self):
        return self.attributes

def elementToObject(parent, node):
    # create an object to represent element node
    object = XMLObject()
    # make object attributes off node attributes
    for key, value in node.attributes.items():
        object.attributes[key] = value
    # make lists of child elements (or ignore them)
    for child in node.childNodes:
        nodeToObject(object, child)
    # add ourselves to parent node
    name = str(node.nodeName)
    l = getattr(parent.elements, name, [])
    l.append(object)
    setattr(parent.elements, name, l)

def attributeToObject(parent, node):
    # should never be called
    pass

def textToObject(parent, node):
    # add this text to parents text content
    parent.text += node.data

def processingInstructionToObject(parent, node):
    # don't do anything with these
    pass

def commentToObject(parent, node):
    # don't do anything with these
    pass

def documentToObject(parent, node):
    elementToObject(parent, node.documentElement)

def documentTypeToObject(parent, node):
    # don't do anything with these
    pass

_map = {
    Node.ELEMENT_NODE: elementToObject,
    Node.ATTRIBUTE_NODE: attributeToObject,
    Node.TEXT_NODE: textToObject,
 #   Node.CDATA_SECTION_NODE:
 #   Node.ENTITY_NODE:
    Node.PROCESSING_INSTRUCTION_NODE: processingInstructionToObject,
    Node.COMMENT_NODE: commentToObject,
    Node.DOCUMENT_NODE: documentToObject,
    Node.DOCUMENT_TYPE_NODE: documentTypeToObject,
#    Node.NOTATION_NODE:
    }

def nodeToObject(parent, node):
    _map[node.nodeType](parent, node)

def simplify_single_entries(object):
    for name in object.getElementNames():
        l = getattr(object.elements, name)
        # set the first subelement (in case it's just one, this is easy)
        setattr(object.first, name, l[0])
        # now do the same for rest
        for element in l:
            simplify_single_entries(element)

def XMLToObjectsFromFile(path):
    return XMLToObjects(parse(path))

def XMLToObjectsFromString(s):
    return XMLToObjects(parseString(s))

def XMLToObjects(document):
    object = XMLObject()
    documentToObject(object, document)
    document.unlink()
    simplify_single_entries(object)
    return object

