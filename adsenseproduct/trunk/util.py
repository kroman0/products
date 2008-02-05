from Products.CMFCore.utils import getToolByName
from config import ADSENSE_MAP

def getCustomerId(context):
    pp = getToolByName(context, 'portal_properties')
    try:
        return pp.adsense_properties.getProperty('customer_id') or None
    except:
        return None

def getCompiledAdsense(context, format, marker=""):
    if not ADSENSE_MAP.has_key(format):
        return marker
    width = ADSENSE_MAP[format]['width']
    height = ADSENSE_MAP[format]['height']
    customer_id = getCustomerId(context)
    if not customer_id:
        return marker
    try:
        return context.adsense_template(customer_id = customer_id \
                                       ,adsense_width=width \
                                       ,adsense_height=height \
                                       ,adsense_format=format \
                                       )
    except:
        return marker

def getAdsenseMap():
    return ADSENSE_MAP