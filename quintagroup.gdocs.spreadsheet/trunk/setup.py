# -*- coding: utf-8 -*-
"""
This module contains the tool of quintagroup.gdocs.spreadsheet
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('quintagroup', 'docs', 'HISTORY.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('quintagroup', 'gdocs', 'spreadsheet', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

tests_require=['zope.testing']

setup(name='quintagroup.gdocs.spreadsheet',
      version=version,
      description="",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='',
      author='Quintagroup',
      author_email='support@quintagroup.com',
      url='http://quintagroup.com/services/plone-development/products/quintagroup.gdocs.spreadsheet',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup', 'quintagroup.gdocs'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        # -*- Extra requirements: -*-
                        ],
      entry_points="""
      # -*- entry_points -*- 
      """,
      )
