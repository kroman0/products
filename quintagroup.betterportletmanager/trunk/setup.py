from setuptools import setup, find_packages

version = '0.1.0'

setup(name='quintagroup.betterportletmanager',
      version=version,
      description="This package overrides standard portlet manager rendrer and @@manage-portlets view",
      long_description="This package overrides standard portlet manager rendrer and @@manage-portlets view",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='quintagroup better portlet manager',
      author='Taras Melnychuk',
      author_email='fenix@quintagroup.com',
      url='http://svn.quintagroup.com/products/quintagroup.portletmanager/trunk/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup',],
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
