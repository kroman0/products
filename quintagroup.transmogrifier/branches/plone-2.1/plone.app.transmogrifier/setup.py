version = '0.1'

import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = ('\n'.join((
    read('README.txt'), ''
    'Detailed Documentation',
    '**********************', '',
    read('plone', 'app', 'transmogrifier', 'atschemaupdater.txt'), '',
    read('plone', 'app', 'transmogrifier', 'workflowupdater.txt'), '',
    read('plone', 'app', 'transmogrifier', 'browserdefault.txt'), '',
    read('plone', 'app', 'transmogrifier', 'criteria.txt'), '',
    read('plone', 'app', 'transmogrifier', 'portaltransforms.txt'), '',

    read('docs', 'HISTORY.txt'), '',

    'Download',
    '********', ''
)))
    
open('doc.txt', 'w').write(long_description)

name='plone.app.transmogrifier'
setup(name=name,
      version=version,
      description="Plone blueprints for collective.transmogrifier pipelines",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='content import filtering plone',
      author='Jarn',
      author_email='info@jarn.com',
      url='http://pypi.python.org/pypi/plone.app.transmogrifier',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.transmogrifier',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
