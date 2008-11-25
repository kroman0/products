from urllib2 import urlopen
from urllib  import quote as urlquote

from OFS.ObjectManager import BadRequestException

def ping_google(url, sitemap_id):
    """Ping sitemap to Google"""
    sitemap_url = urlquote(url + "/" + sitemap_id)
    g = urlopen('http://www.google.com/webmasters/sitemaps/ping?sitemap='+sitemap_url)
    result = g.read()
    g.close()
    return 0
