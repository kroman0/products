import os
import socket
import sys
from paste.script.appinstall import Installer as BaseInstaller
from paste.fileapp import FileApp
from paste import urlparser
from paste import request
from paste.httpexceptions import HTTPNotFound
from spider import webmirror

class PackageProxyApp(object):

    def __init__(self, index_url=None, pack_dir=None):
        if not index_url: 
            print "No repository index provided"
            sys.exit()
        if not pack_dir:
            print "No packages cache directory provided"
            sys.exit()
        if not os.path.isdir(pack_dir):
            print 'You must create the %r directory' % pack_dir
            sys.exit()
        self.index_url = index_url
        self.pack_dir = pack_dir

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '').strip()
        path_parts = path.split('/')
        if len(path_parts) > 1 and path_parts[1] == "favicon.ico":
            return HTTPNotFound()(environ, start_response)
        filename = self.checkCache(path)
        if filename is None:
            return HTTPNotFound()(environ, start_response)
        return FileApp(filename)(environ, start_response)

    def checkCache(self, path):   
        pth = self.pack_dir + path
        pth1 = pth
        if not (path[-3:] in ['tgz','.gz','egg','zip','exe']): 
            pth1 = pth + 'index.html'
        else:
            pth = '/'.join(pth.split('/')[:-1])
        if not os.path.exists(pth1):
            webmirror(pth,1,self.index_url+path,0,1)
        if pth1:
            return pth1
        return pth

def app_factory(global_config, **local_conf):
    # Grab config from wsgi .ini file. If not specified, config.py's values
    # take over.
    pack_dir = local_conf.get('pack_directory', None)
    index_url = local_conf.get('index', None)
    return PackageProxyApp(index_url, pack_dir)

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