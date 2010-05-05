from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import *
from Products.ATContentTypes.content.base import ATCTContent


from quintagroup.referencedatagridfield import PKG_NAME
from quintagroup.referencedatagridfield import ReferenceDataGridField
from quintagroup.referencedatagridfield import ReferenceDataGridWidget

class ReferenceDataGridDemoType(ATCTContent):
    """ Simple ReferenceDataGridField demo."""
    security = ClassSecurityInfo()
    schema = BaseSchema + Schema((

        ReferenceDataGridField('DemoReferenceDataGridField',
            schemata='default',
            widget = ReferenceDataGridWidget(
                label = "Reference DataGrid Field(s)",
                visible = {'edit' : 'visible', 'view' : 'visible'}
            )
        ),
    ))

    meta_type = portal_type = archetype_name = 'ReferenceDataGridDemoType'

registerType(ReferenceDataGridDemoType, PKG_NAME)
