from setuptools import setup, find_packages
import os

version = '0.1'

tests_require=['zope.testing']

setup(name='quintagroup.zopeskel.blayer',
      version=version,
      description="Browser Layout subtemplate for Archetype template",
      long_description=open(os.path.join("docs", "README.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='ZopeSkel archetype subtemplate',
      author='Quintagroup',
      author_email='mylan at quintagroup.com',
      url='http://svn.quintagroup.com/products/quintagroup.zopeskel.blayer',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup', 'quintagroup.zopeskel'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'ZopeSkel',
          'PasteScript>=1.6.3',
          # -*- Extra requirements: -*-
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'quintagroup.zopeskel.blayer.tests.test_suite',
      setup_requires=['setuptools',],
      entry_points="""
      [zopeskel.zopeskel_sub_template]
      browserlayer = quintagroup.zopeskel.blayer:BrowserLayer
      # -*- Entry points: -*-
      """,
      )
