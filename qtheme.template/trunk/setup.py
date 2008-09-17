from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='qtheme.template',
      version=version,
      description="Quintagroup theme template for Plone 3 with nested namespace",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='ZopeSkel theme template Quintagroup',
      author='Quintagroup',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'ZopeSkel',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
          [paste.paster_create_template]
          qplone3_theme = qthemetemplate:qPlone3Theme

          [zopeskel.zopeskel_sub_template]
          skin_layer    = qthemetemplate.localcommands.subtemplates:SkinLayerSubTemplate
          css_resource = qthemetemplate.localcommands.subtemplates:CSSSubTemplate
          js_resource = qthemetemplate.localcommands.subtemplates:JSSubTemplate
          viewlet_order = qthemetemplate.localcommands.subtemplates:ViewletOrderSubTemplate
          viewlet_hidden = qthemetemplate.localcommands.subtemplates:ViewletHiddenSubTemplate

          [distutils.setup_keywords]
          theme_vars = qthemetemplate:assert_dict

          [egg_info.writers]
          theme_vars.txt = qthemetemplate:write_map

      # -*- Entry points: -*-
      """,
      )
