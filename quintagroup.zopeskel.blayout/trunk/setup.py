from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='quintagroup.zopeskel.blayout',
      version=version,
      description="Browser Layout subtemplate for Archetype template",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='ZopeSkel archetype subtemplate',
      author='Quintagroup',
      author_email='mylan at quintagroup.com',
      url='http://svn.quintagroup.com/paroducts/quintagroup.zopeskel.blayout',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup', 'quintagroup.zopeskel'],
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
