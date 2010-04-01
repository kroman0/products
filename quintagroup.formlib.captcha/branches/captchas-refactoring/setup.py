from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='quintagroup.formlib.captcha',
      version=version,
      description="Captcha field for formlib based on quintagroup.captcha.core package",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone formlib captcha',
      author='Vitaliy Podoba',
      author_email='piv@quintagroup.com',
      url='http://svn.plone.org/svn/plone/plone.app.example',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup', 'quintagroup.formlib'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'zope.formlib',
          'quintagroup.captcha.core',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
