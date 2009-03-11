from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='quintagroup.mobileextender',
      version=version,
      description="Extend some AT content types with mobile_text field and overlap appropriate content types views",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone mobile quintagroup',
      author='Quintagroup',
      author_email='support@quintagroup.com',
      url='http://svn.quintagroup.com/products/quintagroup.mobileextender',
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
