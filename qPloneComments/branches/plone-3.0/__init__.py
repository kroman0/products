from AccessControl import allow_module
from AccessControl.Permission import registerPermissions

# Feed our monkeys :-)
from Products.qPloneComments import patch

allow_module('Products.qPloneComments.utils')

registerPermissions((('Moderate Discussion', (), ('Manager',)),))
