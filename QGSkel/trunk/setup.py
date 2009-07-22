from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='QGSkel',
      version=version,
      description="Zope skels by quintagroup",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Volodymyr Cherepanyak',
      author_email='<support at quintagroup.com>',
      url='http://quintagroup.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
