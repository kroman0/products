version = '0.1'

import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = ('\n'.join((
    read('README.txt'), ''
    'Detailed Documentation',
    '**********************', '',
    read('collective', 'transmogrifier', 'transmogrifier.txt'), '',
    read('collective', 'transmogrifier', 'genericsetup.txt'), '',

    'Default section blueprints',
    '**************************',
    read('collective', 'transmogrifier', 'sections', 'constructor.txt'), '',
    read('collective', 'transmogrifier', 'sections', 'codec.txt'), '',
    read('collective', 'transmogrifier', 'sections', 'inserter.txt'), '',
    read('collective', 'transmogrifier', 'sections', 'condition.txt'), '',
    read('collective', 'transmogrifier', 'sections', 'manipulator.txt'), '',
    read('collective', 'transmogrifier', 'sections', 'splitter.txt'), '',
    read('collective', 'transmogrifier', 'sections', 'savepoint.txt'), '',
    read('collective', 'transmogrifier', 'sections', 'csvsource.txt'), '',

    read('docs', 'HISTORY.txt'), '',

    'Download',
    '********', ''
)))
    
open('doc.txt', 'w').write(long_description)

name='collective.transmogrifier'
setup(name=name,
      version=version,
      description='A configurable pipeline, aimed at transforming content for '
                  'import and export',
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Zope2",
        "Framework :: Zope3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='content import filtering',
      author='Jarn',
      author_email='info@jarn.com',
      url='http://pypi.python.org/pypi/collective.transmogrifier',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
