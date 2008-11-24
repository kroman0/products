"""Common configuration constants
"""

PROJECTNAME = 'qPloneGoogleSitemaps'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'Sitemap': 'qPloneGoogleSitemaps: Add Sitemap',
}

SITEMAPS_LIST = ['content','mobile','news']

ping_googlesitemap = 'pingGoogleSitemap'

AVAILABLE_WF_SCRIPTS = [ping_googlesitemap, '']

try:
    from Products.DCWorkflow.events import AfterTransitionEvent
except ImportError:
    IS_PLONE_3 = False
else:
    IS_PLONE_3 = True
