from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='quintagroup.referencedatagridfield',
      version=version,
      description="Mix of Reference and DataGrid fields",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='ReferenceField DataGridField Archetypes',
      author='Quintagroup',
      author_email='talk@quintagroup.com',
      url='http://svn.quintagroup.com/products/quintagroup.referencedatagridfield',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.DataGridField==1.6.1',
          'Products.OrderableReferenceField',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
