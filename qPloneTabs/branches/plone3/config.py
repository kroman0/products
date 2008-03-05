from Products.CMFCore import permissions

VIEW_PERMISSION = permissions.ManagePortal

PROJECTNAME    = 'qPloneTabs'
SKINS_DIR      = 'skins'

GLOBALS        = globals()

PROPERTY_SHEET = 'tabs_properties'
SHEET_TITLE    = 'Portal Tabs Properties'
FIELD_NAME     = 'titles'
PROPERTY_FIELD = ['portal_tabs|Portal Tabs Configuration', 'portal_footer|Portal Footer Configuration']

""" Example javascript
{'id'          : 'test.js',
 'expression'  : 'python: member is not None',
 'inline'      : False,
 'enabled':    : True,
 'cookable'    : True,
 'compression' : 'safe',
 'cacheable'   : True}
"""

JAVASCRIPTS = []

""" Example css
{'id'          : 'test.css',
 'expression'  : 'python: member is not None',
 'media'       : 'screen',
 'rel'         : 'stylesheet',
 'title'       : 'example styles',
 'rendering'   : 'import',
 'enabled':    : True,
 'cookable'    : True,
 'compression' : 'safe',
 'cacheable'   : True}
"""

CSSES = [{'id'          : 'qplonetabs.css',
          'expression'  : '',
          'media'       : 'screen',
          'rel'         : 'stylesheet',
          'title'       : 'qPloneTabs styles',
          'rendering'   : 'import',
          'enabled'     : True,
          'cookable'    : True,
          'compression' : 'safe',
          'cacheable'   : True}]


""" Example kss
{'id'          : 'test.kss',
 'expression'  : 'python: member is not None',
 'enabled':    : True,
 'cookable'    : True,
 'compression' : 'safe',
 'cacheable'   : True}
"""

KSSES = [{'id'          : 'qplonetabs.kss',
          'expression'  : '',
          'enabled'     : True,
          'cookable'    : True,
          'compression' : 'safe',
          'cacheable'   : True},]

