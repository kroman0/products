import os
import socket
import sys
from paste.script.appinstall import Installer as BaseInstaller
from paste.fileapp import FileApp
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
        filename = self.checkCache(path)        
        if path.split('/')[0] == "favicon.ico":
                return HTTPNotFound()(environ, start_response)
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