# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2005-11-23 12:35:33
# Copyright: quintagroup.com

from Products.CMFCore.DirectoryView import DirectoryView, registerDirectory, createDirectoryView
from Products.Archetypes.public import *
from string import split, index
from os import listdir, walk
from epydoc.cli import cli
from os.path import isdir
import Products
import sys

from config import *

schema=BaseFolderSchema

class PloneEpydoc(BaseFolder):

    schema=schema
    archetype_name=ARCHETYPENAME
    id=TOOLID

    def __init__(self):
        """"""
        BaseFolder.__init__(self, self.id)

    def getProductModules(self, path):
        """"""
        modules = []
        for root, dirs, files in walk(path):
            root_list = split(root, '/')
            if not 'tests' in root_list:
                root_list = root_list[index(root_list, 'Products'):] #XXX FIXME
                module_path = '.'.join(root_list)
                for f in files[:]:
                    if f[-3:] == '.py':
                        f = f[:index(f, '.')]
                        modules.append(module_path+'.'+f)
        return modules

    def createDocumentationDirectoryViews(self, product):
        """"""
        try:
            registerDirectory(DOCUMENTATION_DIR, GLOBALS)
        except OSError, ex:
            if ex.errno == 2: # No such file or directory
                return
            raise

        if not product in self.objectIds():
            createDirectoryView(self, '/'.join([PROJECTNAME,DOCUMENTATION_DIR, product]))

    def generate(self, product, **properties):
        """"""
        sys.argv = []
        modules = []
        sys.argv.append('xxx')
        sys.argv.append('--no-private')
        sys.argv.append('--noframes')
        sys.argv.append('--target='+DOCUMENTATION_PATH+product)
        for k in properties.keys():
            sys.argv.append('--'+k+'='+properties[k])

        modules = self.getProductModules(PRODUCTS_HOME+product)
        for m in modules:
            sys.argv.append(m)
        cli()
        self.write_content_file_types(DOCUMENTATION_PATH+product)
        self.createDocumentationDirectoryViews(product)

    def write_object_type(self, path, obj_name, obj_type):
        """"""
        file = open(path+'/.objects', 'a')
        data = obj_name+' : '+obj_type+'\n'
        file.write(data)

    def write_content_file_types(self, path):
        """"""
        for obj in listdir(path):
            if isdir(path+'/'+obj):
                dir_path = path+'/'+obj
                self.write_content_file_types(dir_path)

            self.write_object_type(path, obj, 'File')

registerType(PloneEpydoc)