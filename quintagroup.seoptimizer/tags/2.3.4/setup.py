# -*- coding: utf-8 -*-
"""
This module contains the tool of quintagroup.seoptimizer
"""
import os
from setuptools import setup, find_packages


version = '2.3.4'

setup(name='quintagroup.seoptimizer',
      version=version,
      description="Quintagroup Search Engine Optimization Tool",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "INSTALL.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),

      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Myroslav Opyr, Volodymyr Romaniuk, Mykola Kharechko, Vitaliy Podoba, Volodymyr Cherepanyak, Taras Melnychuk, Vitaliy Stepanov',
      author_email='support@quintagroup.com',
      url='http://quintagroup.com/services/plone-development/products/qSEOptimizer/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup'],
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
