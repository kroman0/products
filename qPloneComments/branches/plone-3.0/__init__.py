from AccessControl import allow_module

# Feed our monkeys :-)
from Products.qPloneComments import patch

allow_module('Products.qPloneComments.utils')
