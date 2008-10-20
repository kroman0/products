from zope.component import getMultiAdapter

from AccessControl import ClassSecurityInfo

from Products.CMFCore.permissions import View

from Products.Archetypes.Widget import StringWidget
from Products.Archetypes.Registry import registerWidget


class ReadonlyStringWidget(StringWidget):
    _properties = StringWidget._properties.copy()
    _properties.update({
        'macro' : "readonlystring",
        })

    security = ClassSecurityInfo()
    
    security.declareProtected(View, 'readonly')
    def readonly(self, context, request):
        portal_state = getMultiAdapter((context, request), name="plone_portal_state")
        if portal_state.anonymous():
            return None
        else:
            return '1'

registerWidget(ReadonlyStringWidget,
               title='ReadonlyString',
               description=('Renders a HTML readonly text input box which '
                            'accepts a single line of text'),
               used_for=('Products.Archetypes.Field.StringField',)
               )
