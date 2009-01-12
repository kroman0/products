## Script (Python) "listMetaTags"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=List Dublin Core for '<meta>' tags
##

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

site_props = getToolByName(context, 'portal_properties').site_properties
exposeDCMetaTags = site_props.getProperty('exposeDCMetaTags',True)

metadataList = [
    # dublic core accessor name, metadata name
    ('qSEO_Description', 'description'),
    ('qSEO_Keywords',    'keywords'),
    ('qSEO_Robots',      'robots'),
    ('qSEO_Distribution','distribution'),
]

returnList = []
if exposeDCMetaTags: 
        metadataList.append(('qSEO_Distribution', 'DC.distribution'))
        metadataList.append(('Description',      'DC.description'))
        metadataList.append(('Subject',          'DC.subject'))
        metadataList.append(('Creator',          'DC.creator'))
        metadataList.append(('Contributors',     'DC.contributors'))
        metadataList.append(('Publisher',        'DC.publisher'))
        metadataList.append(('CreationDate',     'DC.date.created'))
        metadataList.append(('ModificationDate', 'DC.date.modified'))
        metadataList.append(('Type',             'DC.type'))
        metadataList.append(('Format',           'DC.format'))
        metadataList.append(('Language',         'DC.language'))
        metadataList.append(('Rights',           'DC.rights'))

for accessor, key in metadataList:
    method = getattr(context, accessor, None)
    if not callable(method):
        # ups
        continue

    # Catch AttributeErrors raised by some AT applications
    try:
        value = method()
    except AttributeError:
        value = None

    if not value:
        # no data
        continue
    if accessor == 'Publisher' and value == 'No publisher':
        # No publisher is hardcoded (XXX: still?)
        continue
    if same_type(value, ()) or same_type(value, []):
        # convert a list to a string
        value = ', '.join(value)
    returnList.append( (key, value) )

# Portions of following code was copy/pasted from the listMetaTags script from
# CMFDefault.  This script is licensed under the ZPL 2.0 as stated here:
# http://www.zope.org/Resources/ZPL
# Zope Public License (ZPL) Version 2.0
# This software is Copyright (c) Zope Corporation (tm) and Contributors. All rights reserved.
created = context.CreationDate()

effective = context.EffectiveDate()
if effective and effective != 'None':
    effective = DateTime(effective)
else:
    effective = None

expires = context.ExpirationDate()
if expires and expires != 'None':
    expires = DateTime(expires)
else:
    expires = None

#   Filter out DWIMish artifacts on effective / expiration dates
eff_str = ( effective and effective.year() > 1000
                      and effective != created ) and effective.Date() or ''
exp_str = ( expires and expires.year() < 9000 ) and expires.Date() or ''

if exp_str or exp_str:
    returnList.append( ( 'DC.date.valid_range'
                    , '%s - %s' % ( eff_str, exp_str ) ) )

return returnList
