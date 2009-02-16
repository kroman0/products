from setuptools import setup, find_packages
import os

setup(name='quintagroup.pingtool',
      version=open(os.path.join("quintagroup", "pingtool", "version.txt")).read(),
      description="quintagroup.pingtool is a simple tool to enable pinging of external feed agregators for Plone 3.1.x",
      long_description=open("README.txt").read() + "\n" +
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
      url='http://svn.quintagroup.com/products/quintagroup.pingtool/trunk',
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
