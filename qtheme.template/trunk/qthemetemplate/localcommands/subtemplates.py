"""
Local templates for the qplone3_theme
"""
import os, sys
from zopeskel.base import var
from zopeskel.localcommands import ZopeSkelLocalTemplate
from qthemetemplate.localcommands import QThemeSubTemplate

class SkinLayerSubTemplate(QThemeSubTemplate):
    """
    A Plone Skin layer skeleton
    """
    _template_dir = 'templates/skinlayer'
    summary = "A Plone 3 Skin Layer"
    

    vars = [
      var('layer_name', 'Skin Layer name (should not contain spaces)',
           default="skin_layer"),
           ]


class SkinSublayerSubTemplate(QThemeSubTemplate):
    """ Server for add Skin Layer to skin-path
        in profiles/default/skins.xml
    """

    _template_dir = 'templates/skinsublayer'
    summary = "A Plone 3 Skin SubLayer registration in GS' skins.xml"
    marker_name = "extra sublayer stuff goes here"
    
    vars = [
        var('sublayername', 'Skin Layer name (should not contain spaces)', default="skin_layer"),
        var('insert_type', 'Where insert the layer ("after" or "before")', default="after"),
        var('insert_control_layer',
            'Layer after or before which your layer will be inserted, "*" accepted, which mean all',
            default='custom'),
           ]


class CSSSubTemplate(QThemeSubTemplate):
    """
    A Plone CSS resource skeleton
    """
    _template_dir = 'templates/cssresource'
    summary = "A Plone 3 CSS resource template"
    

    vars = [
      var('css_resource_name', 'Name of CSS resource',
           default="main.css"),
      var('css_file_path', 'Path to CSS file'),
      var('cssreg_media', 'Optional.Possible values:screen,print,projection,handheld',
           default="screen", ),
      var('cssreg_rel', 'Optional', default="stylesheet"),
      var('cssreg_rendering', 'Optional.Possible values:import,link,inline', default="inline"),
      var('cssreg_cacheable', '', default="True"),
      var('cssreg_compression', 'Compression type', default="safe"),
      var('cssreg_cookable', 'Boolean, aka merging allowed', default="True"),
      var('cssreg_enables', 'Optional.Boolean', default="1"),
      var('cssreg_expression', 'Optional.A tal condition.', default=""),
           ]

    def pre(self, command, output_dir, vars):
        """ Set 'css_resource_content' value from css_file_path
        """
        
        if not os.path.isfile(vars['css_file_path']):
            raise ValueError('%s - wrong file path for css resource' % \
                             vars['css_file_path'] )
        vars['css_resource_content'] = file(vars['css_file_path'],'rb').read()

