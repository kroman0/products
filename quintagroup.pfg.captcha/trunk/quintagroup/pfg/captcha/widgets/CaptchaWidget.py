from Products.Archetypes.Widget import StringWidget
from Products.Archetypes.Registry import registerWidget

class CaptchaWidget(StringWidget):
    _properties = StringWidget._properties.copy()
    _properties.update( {'macro' : "captchaField_widget"} )


registerWidget(CaptchaWidget,
               title = 'Captcha widget',
               description= ('Renders captcha image and string input',),
               used_for = ('quintagroup.pfg.captcha.content.CaptchaField',)
              )