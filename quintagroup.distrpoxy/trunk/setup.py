from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='quintagroup.distproxy',
      version=version,
      description="quintgroup.distproxy is a smart mirror for dist.plone.org",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Volodymyr Cherepanyak, Quintagroup',
      author_email='<support at quintagroup.com>',
      url='http://svn.quintagroup.com/products/quintagroup.distrpoxy',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'PasteScript',
          'PasteDeploy',
          # -*- Extra requirements: -*-
      ],
      entry_points={
          'paste.app_factory': [
              'main = quintagroup.distproxy.wsgi:app_factory',
              'static = quintagroup.distproxy.wsgi:make_static',
              ],
          },
      )
