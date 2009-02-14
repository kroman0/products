from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='quintagroup.sectionstyle',
      version=version,
      description="Inserts extra html class (taken from context properties) into body element.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone web html class',
      author='Vitaliy Podoba',
      author_email='piv@quintagroup.com',
      url='http://svn.quintagroup.com/products/quintagroup.sectionstyle',
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
