from setuptools import setup, find_packages
import os

version = '1.0.1'

setup(name='quintagroup.pagetemplateshrink',
      version=version,
      description="Pagetemplates monkeypatch to shrink rendered HTML",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Volodymyr Cherepanyak',
      author_email='support@quintagroup.com',
      url='http://www.quintagroup.com',
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
