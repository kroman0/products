from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='quintagroup.pfg.captcha',
      version=version,
      description="quintagroup.pfg.captcha is a package that allows to add captcha field to the form, created with PloneFormGen product.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone captcha PloneFormGen',
      author='Quintagroup',
      author_email='support@quintagroup.com',
      url='http://projects.quintagroup.com/products/wiki/qPloneCaptchaField',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup', 'quintagroup.pfg'],
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
