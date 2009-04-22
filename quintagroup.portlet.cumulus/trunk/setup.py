from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='quintagroup.portlet.cumulus',
      version=version,
      description="This package allows you to display your site's tags using a Flash movie that rotates them in 3D. This is the WordPress WP-Cumulus plugin ported to Plone.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone portlet flash tag cloud',
      author='Bohdan Koval',
      author_email='koval@quintagroup.com',
      url='http://svn.quintagroup.com/products/quintagroup.portlet.cumulus',
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
      """,
      )
