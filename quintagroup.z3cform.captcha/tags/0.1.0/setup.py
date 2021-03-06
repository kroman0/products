from setuptools import setup, find_packages
import os

version = '0.1.0'

setup(name='quintagroup.z3cform.captcha',
      version=version,
      description="Captcha field for z3cform based on quintagroup.plonecaptchas package",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone z3c form captcha',
      author='Melnychuk Taras',
      author_email='support@quintagroup.com',
      url='http://quintagroup.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup', 'quintagroup.z3cform'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # uncomment next packages only if they will be downloaded from some package index
          # 'quintagroup.plonecaptchas', 
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
