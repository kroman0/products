"""
Local templates for the qplone3_theme
"""
import os, sys, re
from zopeskel.base import var
from zopeskel.localcommands import ZopeSkelLocalTemplate
from qthemetemplate.localcommands import QThemeSubTemplate

RESP = re.compile("\s+")


class SkinLayerSubTemplate(QThemeSubTemplate):
    """
    A Plone Skin layer skeleton
    """
    _template_dir = 'templates/skinlayer'
    summary = "A Plone 3 Skin Layer"

    compo_template_markers = [
        ('layer4Skin',   'extra layer stuff goes here'),
    ]

    vars = [
      var('layer_name', 'Skin Layer name (should not contain spaces)',
           default="skin_layer"),
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
        super(CSSSubTemplate, self).pre(command, output_dir, vars)

        if not os.path.isfile(vars['css_file_path']):
            raise ValueError('%s - wrong file path for css resource' % \
                             vars['css_file_path'] )
        vars['css_resource_content'] = file(vars['css_file_path'],'rb').read()


class JSSubTemplate(QThemeSubTemplate):
    """
    A Plone JS resource skeleton
    """
    _template_dir = 'templates/jsresource'
    summary = "A Plone 3 JS resource template"
    

    vars = [
      var('js_resource_name', 'Name of JS resource', default="foo.js"),
      var('js_file_path', 'Path to JS file'),
      var('jsreg_inline', 'Optional.Boolean', default="False"),
      var('jsreg_cacheable', '', default="True"),
      var('jsreg_compression', 'Compression type.Possible:none,safe,full,safe-encode,full-encode',
          default="safe"),
      var('jsreg_cookable', 'Boolean, aka merging allowed', default="True"),
      var('jsreg_enables', 'Optional.Boolean', default="1"),
      var('jsreg_expression', 'Optional.A tal condition.', default=""),
           ]

    def pre(self, command, output_dir, vars):
        """ Set 'js_resource_content' value from js_file_path
        """
        super(JSSubTemplate, self).pre(command, output_dir, vars)
        
        if not os.path.isfile(vars['js_file_path']):
            raise ValueError('%s - wrong file path for js resource' % \
                             vars['js_file_path'] )
        vars['js_resource_content'] = file(vars['js_file_path'],'rb').read()


class ViewletOrderSubTemplate(QThemeSubTemplate):
    """
    A Plone Order Viewlet skeleton
    """
    _template_dir = 'templates/viewlet'
    summary = "A Plone 3 Order Viewlet template"
    
    # list of 2 item tuple -
    # (compotemplate_name, compo marker), for ex.:
    compo_template_markers = [
        ('order_profiles',   'object stuff goes here'),
    ]

    vars = [
      var('viewlet_name', "Viewlet name", default='example'),
      var('viewlet_manager_interface', "Viewlet manager interface",
          default="plone.app.layout.viewlets.interfaces.IPortalHeader"),
      var('viewlet_manager_name', "Viewlet manager name", default='plone.portalheader'),
      var('viewlet_permission', "Viewlet permission", default="zope2.View"),

      var('insert_type', 'Where insert the viewlet ("after" or "before")', default="after"),
      var('insert_control_viewlet', 'Viewlet after or before which your viewlet will be inserted, ' \
          '"*" accepted, which mean all', default='*'),

      var('layer_interface', "Layer interface for registry this viewlet on", default=""),
      var('layer_name', "Layer name for registry this viewlet on", default=""),
      var('skinname', "Skin name, for bind viewlet to, '*' - mean for all", default=""),
      var('skinbase', "Base skin, for get viewlets from", default=""),
           ]

    def pre(self, command, output_dir, vars):
        """ Set 'css_resource_content' value from css_file_path
        """

        vn_lower_nospc = RESP.sub('',vars['viewlet_name']).lower()
        vn_lower_under = RESP.sub('_',vars['viewlet_name']).lower()
        VnCamel = ''.join([i.capitalize() for i in vars['viewlet_name'].split()])
        vars['viewlet_class_name'] = VnCamel
        vars['viewlet_interface_name'] = "I"+VnCamel
        vars['viewlet_template_name'] = vn_lower_nospc+'_viewlet.pt'

        viewlet_profile_marker = "[order_%s] viewlet stuff goes here" % \
            '.'.join([vars['viewlet_manager_name'], vars['skinname'], vars['skinbase']])

        vars['viewlet_profile_marker'] = viewlet_profile_marker
        self.compo_template_markers.append(
            ('viewlet_profiles',viewlet_profile_marker))


class ViewletHiddenSubTemplate(QThemeSubTemplate):
    """
    A Plone Hidden Viewlet skeleton
    """
    _template_dir = 'templates/viewlet_hidden'
    summary = "A Plone 3 Hidden Viewlet template"
    compo_template_markers = [
        ('hidden_profiles',   'object stuff goes here'),
    ]
    
    vars = [
      var('viewlet_name', "Viewlet name", default='plone.global_sections'),
      var('viewlet_manager_name', "Viewlet manager name", default='plone.portalheader'),
      var('skinname', "Skin name, for bind viewlet to, may be '*'", default=""),
           ]

    def pre(self, command, output_dir, vars):
        """ Set 'css_resource_content' value from css_file_path
        """
         
        viewlet_profile_marker = "[hidden_%s] viewlet stuff goes here" % \
            '.'.join([vars['viewlet_manager_name'], vars['skinname']])

        vars['viewlet_profile_marker'] = viewlet_profile_marker
        self.compo_template_markers.append(
            ('viewlet_hidden_profiles',viewlet_profile_marker))

