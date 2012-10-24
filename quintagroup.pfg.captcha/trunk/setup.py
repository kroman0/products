from setuptools import setup, find_packages
import os

version = '1.0.5'

setup(name='quintagroup.pfg.captcha',
      version=version,
      description="quintagroup.pfg.captcha is a package that allows "
                  "to add captcha field to PloneFormGen forms.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 3.2",
        "Framework :: Plone :: 3.3",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone captcha PloneFormGen',
      author='Quintagroup',
      author_email='support@quintagroup.com',
      url='http://projects.quintagroup.com/products/wiki/'
          'quintagroup.pfg.captcha',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup', 'quintagroup.pfg'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'quintagroup.captcha.core',
          'Products.PloneFormGen',
          # -*- Extra requirements: -*-
          # 'zope.event',
          # 'zope.lifecycleevent',
          # 'Products.CMFCore',
          # 'Products.CMFPlone',
          # 'Products.Archetypes',
          # 'Products.ATContentTypes',
          # 'Products.validation',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
