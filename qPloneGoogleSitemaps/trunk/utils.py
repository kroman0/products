from urllib2 import urlopen
from urllib  import quote as urlquote

from OFS.ObjectManager import BadRequestException

from Products.qPloneGoogleSitemaps.config import testing

def ping_google(url, sitemap_id):
    """Ping sitemap to Google"""
    resurl = url + "/" + sitemap_id
    sitemap_url = urlquote(resurl)
    g = urlopen('http://www.google.com/webmasters/sitemaps/ping?sitemap='+sitemap_url)
    result = g.read()
    g.close()
    if testing:
        print "Pinged %s sitemap to google" % resurl
    return 0
