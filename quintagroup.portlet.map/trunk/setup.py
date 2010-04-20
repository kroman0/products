from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='quintagroup.portlet.map',
      version=version,
      description="Quintagroup Google Map portlet",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='\x1b[B\x1b[B\x1b[BGoogleMaps portlet plone Product.Maps',
      author='mylan',
      author_email='support@quintagroup.com',
      url='http://svn.quintagroup.com/products/quintagroup.portlet.map',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup', 'quintagroup.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
