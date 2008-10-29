from setuptools import setup, find_packages

version = '0.1.0'

setup(name='quintagroup.portletmanager',
      version=version,
      description="Quintagroup portlet manager",
      long_description="""Quintagroup portlet manager""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='quintagroup portlet manager',
      author='Taras Melnychuk',
      author_email='fenix@quintagroup.com',
      url='http://svn.quintagroup.com/products/quintagroup.portletmanager/trunk/',
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
