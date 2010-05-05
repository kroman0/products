#from Products.Archetypes import atapi
import logging
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Registry import registerField, registerWidget

from Products.DataGridField.DataGridField import DataGridField
from Products.DataGridField.DataGridWidget import DataGridWidget

# Logger object
#logger = logging.getLogger('ReferenceDataGridField')
#logger.debug("ReferenceDataGrid loading")

class ReferenceDataGridWidget(DataGridWidget):
    _properties = DataGridWidget._properties.copy()
    _properties.update({
        'macro' : "referencedatagridwidget",
        })

class ReferenceDataGridField(DataGridField):
    _properties = DataGridField._properties.copy()
    _properties.update({
        'columns' : ('title', 'link_uid'),
        'widget': ReferenceDataGridWidget,
        })

registerWidget(
    ReferenceDataGridWidget,
    title='DataGrid Reference',
    used_for=('quintagroup.referencedatagridfield.ReferenceDataGridField',)
    )

registerField(
    ReferenceDataGridField,
    title="DataGrid Reference Field",
    description=("Reference DataGrid field.")
    )
