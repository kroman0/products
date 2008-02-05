from Products.CMFCore import CMFCorePermissions
from Products.Archetypes.utils import DisplayList

SKINS_DIR = 'skins'
GLOBALS = globals()
PROJECTNAME = 'qPingTool'

ADD_PERMISSION = CMFCorePermissions.ManagePortal

TOOL_ID = 'portal_pingtool'

TOOL_ICON = 'tool.gif'

RSS_LIST = DisplayList((('Blog','Blog'),('RSS','RSS1'),('RSS2','RSS2')))

CONFIGURATION_CONFIGLET = 'pingtool_config'
SITES_LIST=(('weblogs',    'www.weblogs.com (blog url)',                'http://rpc.weblogs.com/'),
            ('pingomatic', 'rpc.pingomatic.com (blog url)',             'http://rpc.pingomatic.com/'),
            ('blogs',      'blo.gs (blog url)',                         'http://ping.blo.gs/'),
            ('technorati', 'technorati.com (blog url)',                 'http://rpc.technorati.com/rpc/ping'),
            ('myyahoo',    'my.yahoo.com (blog url)',                   'http://api.my.yahoo.com/RPC2'),
            ('blogrolling','blogrolling.com (blog url)',                'http://rpc.blogrolling.com/pinger/'),
            ('syndic8',    'syndic8.com (blog url manual submittion)',  'http://ping.syndic8.com/xmlrpc.php'),
            ('blogshares', 'blogshares.com (blog url manual submittion)','http://www.blogshares.com/rpc.php'),
            ('newsisfree', 'newsisfree.com (blog url)',                 'http://www.newsisfree.com/xmlrpctest.php3'),
            ('blogstreet', 'blogstreet.com (blog url manual submittion)','http://www.blogstreet.com/xrbin/xmlrpc.cgi'),
            ('blogdigger', 'blogdigger.com (blog url)',                 'http://www.blogdigger.com/RPC2'),
            ('rootblog',   'rootblog.com (blog url manual submittion)', 'http://ping.rootblog.com/rpc.php'),
            ('feedster',   'feedster.com (blog url manual submittion)', 'http://api.feedster.com/ping'),
            ('moreover',   'moreover.com (blog url)',                   'http://api.moreover.com/RPC2')
            )