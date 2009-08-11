# -*- coding: utf-8 -*-
"""
This module contains the tool of quintagroup.pingtool
"""
import os
from setuptools import setup, find_packages

version = '1.1.4'

setup(name='quintagroup.pingtool',
      version=version,
      description="quintagroup.pingtool is a simple tool to enable pinging of external feed agregators for Plone 3.1.x",
      long_description=open("README.txt").read() + "\n\n" +
                       open(os.path.join("docs", "INSTALL.txt")).read() + "\n\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='liebster',
      author_email='support@quintagroup.com',
      url='http://quintagroup.com/services/plone-development/products/ping-tool',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'archetypes.schemaextender',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
