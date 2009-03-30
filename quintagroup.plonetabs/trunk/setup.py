from setuptools import setup, find_packages

version = '0.5b1'

setup(name='quintagroup.plonetabs',
      version=version,
      description="Quintagroup Plone Tabs",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='quintagroup plonetabs',
      author='(c) "Quintagroup": http://quintagroup.com/ , 2008',
      author_email='info@quintagroup.com',
      url='http://projects.quintagroup.com/products/wiki/qPloneTabs',
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
