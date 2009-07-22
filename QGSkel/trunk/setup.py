from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='QGSkel',
      version=version,
      description="Zope skels by quintagroup",
      long_description=open('README.txt').read() + "\n" +
                         open('HISTORY.txt').read(),
      classifiers=[
         "Development Status :: 5 - Production/Stable",
         "Framework :: Zope2",
         "Framework :: Zope3",
         "Intended Audience :: Developers",
         "License :: OSI Approved :: MIT License",
         "Programming Language :: Python",
         "Topic :: Internet :: WWW/HTTP",
         "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
         ],
      keywords='',
      author='Volodymyr Cherepanyak',
      author_email='support at quintagroup.com',
      url='http://quintagroup.com',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [paste.paster_create_template]
      qgplone3_buildout = qgskel:QGPlone3Buildout
      """,
      )
