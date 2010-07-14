from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='quintagroup.blog.star',
      version=version,
      description="Quintagroup customization of collective.blog.star package",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Quintagroup',
      author_email='',
      url='http://svn.quintagroup.com/products/quintagroup.blog.star',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup', 'quintagroup.blog'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.blog.star',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
