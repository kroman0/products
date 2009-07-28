from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='quintagroup.dropdownmenu',
      version=version,
      description="Multilevel portal dropdown menu for Plone sites.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read() +
                       open(os.path.join("quintagroup", "dropdownmenu", "menu.txt")).read() +
                       open(os.path.join("quintagroup", "dropdownmenu", "controlpanel.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='web plone menu',
      author='Vitaliy Podoba',
      author_email='piv@quintagroup.com',
      url='http://svn.quintagroup.com/products/quintagroup.dropdownmenu',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'plone.app.registry',
          'plone.app.z3cform==0.4.6',
          'plone.z3cform==0.5.5',
          'z3c.form==1.9.0',
          'collective.testcaselayer',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
