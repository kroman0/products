import os
import socket
import sys
from time import time
from paste.script.appinstall import Installer as BaseInstaller
from paste.fileapp import FileApp
from paste import urlparser
from paste import request
from paste.httpexceptions import HTTPNotFound
import urllib2

FILES = ['ico','txt','tgz','.gz','egg','zip','exe','cfg']


class PackageProxyApp(object):

    def __init__(self, index_url=None, pack_dir=None, username=None,
                 password=None, realm=None, stimeout=None, ptimeout=None):
        if not index_url: 
            print "No repository index provided"
            sys.exit()
        if not pack_dir:
            print "No packages cache directory provided"
            sys.exit()
        if not os.path.isdir(pack_dir):
            print 'You must create the %r directory' % pack_dir
            sys.exit()
        if username and password:
            # authenticate
            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            top_level_url = index_url
            password_mgr.add_password(realm, top_level_url, username, password)
            handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            opener = urllib2.build_opener(handler)
            urllib2.install_opener(opener)
        if stimeout:
            socket.setdefaulttimeout(float(stimeout))
        self.index_url = index_url
        self.pack_dir = pack_dir
        self.ptimeout = ptimeout or 3600

    def __call__(self, environ, start_response):
        """ serve the static files """
        path = environ.get('PATH_INFO', '').strip()
        path_parts = path.split('/')
        if len(path_parts) > 1 and path_parts[1] == "favicon.ico":
            return HTTPNotFound()(environ, start_response)
        filename = self.checkCache(path[1:])
        if filename is None:
            return HTTPNotFound()(environ, start_response)
        return FileApp(filename)(environ, start_response)

    def checkCache(self, path):
        """check if we already have the file and download it if not"""   
        pth = self.pack_dir + path
        index = 0 
        if not (path[-3:] in FILES): 
            if not os.path.exists(pth):
                os.makedirs(pth) # create dir if it is not there
            # add index.html for supposedly folders
            pth = pth + 'index.html'
            index = 1
        else:
            pth1 = '/'.join(pth.split('/')[:-1])
            if not os.path.exists(pth1):
                os.makedirs(pth1) # create parent dir if it is not there
        url = self.index_url+path
        #if we dont have download it
        if not os.path.exists(pth):
            f = urllib2.urlopen(url)
            lf = open(pth,'wb')
            lf.write(f.read())
            lf.close()
        #if we have the index.html file if it is older the 1 hour update
        elif index and int(time()) - os.path.getmtime(pth) > self.ptimeout:
            try:
                f = urllib2.urlopen(url)
                lf = open(pth,'wb')
                lf.write(f.read())
                lf.close()
            except urllib2.URLError:
                pass      
        return pth

def app_factory(global_config, **local_conf):
    # Grab config from wsgi .ini file. If not specified, config.py's values
    # take over.
    pack_dir = local_conf.get('pack_directory', None)
    index_url = local_conf.get('index', None)
    username = local_conf.get('username', None)
    password = local_conf.get('password', None)
    realm = local_conf.get('realm', None)
    stimeout = local_conf.get('stimeout', None)
    ptimeout = local_conf.get('ptimeout', None)
    return PackageProxyApp(index_url, pack_dir, username, password, realm, stimeout, ptimeout)

class StaticURLParser(urlparser.StaticURLParser):

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO', '')
        if not path_info:
            return self.add_slash(environ, start_response)
        if path_info == '/':
            # @@: This should obviously be configurable
            filename = 'index.html'
        else:
            filename = request.path_info_pop(environ)
        full = os.path.normcase(os.path.normpath(
            os.path.join(self.directory, filename)))
        if os.path.sep != '/':
            full = full.replace('/', os.path.sep)
        if self.root_directory is not None and not full.startswith(self.root_directory):
            # Out of bounds
            return self.not_found(environ, start_response)
        if not os.path.exists(full):
            if full.endswith('index.html') and not os.path.isfile(full):
                start_response('200 OK', [('Content-Type', 'text/html')])
                return [self.get_index_html()]
            return self.not_found(environ, start_response)
        if os.path.isdir(full):
            # @@: Cache?
            child_root = self.root_directory is not None and \
                self.root_directory or self.directory
            return self.__class__(full, root_directory=child_root,
                                  cache_max_age=self.cache_max_age)(environ,
                                                                   start_response)
        if environ.get('PATH_INFO') and environ.get('PATH_INFO') != '/':
            return self.error_extra_path(environ, start_response)
        if_none_match = environ.get('HTTP_IF_NONE_MATCH')
        if if_none_match:
            mytime = os.stat(full).st_mtime
            if str(mytime) == if_none_match:
                headers = []
                ETAG.update(headers, mytime)
                start_response('304 Not Modified', headers)
                return [''] # empty body

        fa = self.make_app(full)
        if self.cache_max_age:
            fa.cache_control(max_age=self.cache_max_age)
        return fa(environ, start_response)

    def get_index_html(self):
        path = self.directory
        # create sorted lists of directories and files
        names = [i for i in os.listdir(path) if not i.startswith('.')]
        dirs = [i for i in names if os.path.isdir(os.path.join(path, i))]
        dirs.sort()
        files = [i for i in names if os.path.isfile(os.path.join(path, i))]
        files.sort()
        names = dirs + files
        links = '\n'.join(['<li><a href="%s">%s</a></li>' %  (i, i) for i in names])
        template = open(os.path.join(os.path.dirname(__file__), 'index.html')).read()
        return template % {'path': path[len(self.root_directory):], 'links': links}

def make_static(global_conf, document_root, cache_max_age=None):
    """
    Return a WSGI application that serves a directory (configured
    with document_root)

    cache_max_age - integer specifies CACHE_CONTROL max_age in seconds
    """
    if cache_max_age is not None:
        cache_max_age = int(cache_max_age)
    return StaticURLParser(
        document_root, cache_max_age=cache_max_age)


"""
class Installer(BaseInstaller):
    use_cheetah = False
    config_file = 'deployment.ini_tmpl'

    def config_content(self, command, vars):
        import pkg_resources
        module = 'collective.eggproxy'
        if pkg_resources.resource_exists(module, self.config_file):
            return self.template_renderer(
                pkg_resources.resource_string(module, self.config_file),
                vars,
                filename=self.config_file)
"""
