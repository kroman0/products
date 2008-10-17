from xml.dom import minidom

from zope.interface import Interface, implements
from zope.component import adapts

from Products.Archetypes import atapi
from Products.Marshall.config import AT_NS

from quintagroup.transmogrifier.interfaces import IExportDataCorrector
from quintagroup.transmogrifier.adapters.exporting import ReferenceExporter

class IPloneFormMailer(Interface):
    """ Marker interface for PloneFormMailer content type
    """

class PloneFormMailerExporter(ReferenceExporter):
    """ Marshalls PloneFormMailer to XML.
    """
    implements(IExportDataCorrector)
    adapts(IPloneFormMailer)

    def __init__(self, context):
        self.context = context
        self.tales_fnames = ['recipient_name', 'bcc_recipients', 'cc_recipients']
        self.mail_subject_field = 'subject' 

    def __call__(self, data):
        xml = data['data']
        xml = self.exportReferences(xml)
        data['data'] = self.exportFormFields(xml)
        return data

    def exportFormFields(self, data):
        """ Reformat xml file and add Formulator fields.
        """
        # reformat xml tree
        doc = minidom.parseString(data)
        root = doc.documentElement

        # some TALES fields must be exported as value of executed expression
        schema = self.context.Schema()
        for fname in self.tales_fnames:
            nodes = [i for i in root.getElementsByTagName('field') if i.getAttribute('name') == fname]
            for node in nodes:
                root.removeChild(node)
            values = schema[fname].getAccessor(self.context)()
            if not isinstance(values, (list, tuple)):
                values = [values]
            values = filter(None, values)
            for value in values:
                node = doc.createElementNS(AT_NS, "field")
                name_attr = doc.createAttribute("name")
                name_attr.value = fname
                node.setAttributeNode(name_attr)
                value_node = doc.createTextNode(str(value))
                node.appendChild(value_node)
                node.normalize()
                root.appendChild(node)

        # PloneFormMailer overrides standard 'subject' schema field with it's own,
        # which is a subject of a message. That's why it isn't exported as '<dc:subject />'
        # element (it is concerned with current implementation of Marshall's CMF namespaces
        value = atapi.BaseObject.__getitem__(self.context, self.mail_subject_field)
        if value:
            node = doc.createElementNS(AT_NS, "field")
            name_attr = doc.createAttribute("name")
            name_attr.value = mail_subject_field
            node.setAttributeNode(name_attr)
            value_node = doc.createTextNode(str(value))
            node.appendChild(value_node)
            node.normalize()
            root.appendChild(node)

        # append form fields
        fm_doc = minidom.parseString(self.context.form.get_xml())
        root.appendChild(fm_doc.documentElement)

        return doc.toxml('utf-8')
