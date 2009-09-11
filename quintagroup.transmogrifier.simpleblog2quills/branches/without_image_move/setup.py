from setuptools import setup, find_packages
import os

version = '0.2.1'

setup(name='quintagroup.transmogrifier.simpleblog2quills',
      version=version,
      description="Configuration of collective.transmogrifier pipeline for blog migration from SimpleBlog to QuillsEnabled",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Quintagroup',
      author_email='info@quintagroup.com',
      url='http://quintagroup.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup', 'quintagroup.transmogrifier'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'quintagroup.transmogrifier',
          #'Products.Quills'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
