import string,os,urllib,httplib,urlparse,re
import sys

def post_trackback(context,
                   ping_url, 
                   title = "", 
                   src_url = "", 
                   blog_name = "",
                   excerpt = "",
                   agent = "",
                   charset = "",
                   param_charset = ""):
    """
    Sending PING request to ping_url
    """
    params = {"title":    title,\
              "url":      src_url,\
              "blog_name": blog_name,\
              "excerpt": excerpt
             }
    headers = ({"Content-type": "application/x-www-form-urlencoded",
                "User-Agent": agent})


    if param_charset:
        params["charset"] = param_charset
    elif charset:
        headers["Content-type"] = headers["Content-type"] + "; charset=%s"

    #if len(excerpt) > 0:
    #    params["excerpt"] = excerpt

    tb_url_t = urlparse.urlparse(ping_url)

    enc_params = urllib.urlencode(params)

    #check if trackback url contains parameter section(for PyDs!)
    ut = urlparse.urlparse(ping_url)
    if len(ut) >= 4 and ut[4]:
        #add params to parameter section
        enc_params = ut[4] + '&' + enc_params

    host = tb_url_t[1]
    path = tb_url_t[2]

    try:
        con = httplib.HTTPConnection(host)
        con.request("POST", path, enc_params, headers)
    except:
        pass

    return 0,"trackback sent"


def addTrackBack(blog_entry, id, title, url, blog_name, excerpt):
    """ create trackback object """
    blog_entry.invokeFactory(id=id, type_name="TrackBack")
    trback = getattr(blog_entry, id, None)
    trback.update(title = title,
                  url = url,
                  blog_name = blog_name,
                  excerpt = excerpt)

def encodeURLData(data_dict):
    """ encode URL data """
    return urllib.urlencode(data_dict)
