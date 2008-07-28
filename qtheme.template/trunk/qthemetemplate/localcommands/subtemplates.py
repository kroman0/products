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

