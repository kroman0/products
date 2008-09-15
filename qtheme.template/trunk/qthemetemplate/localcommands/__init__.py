"""
Local templates for the qplone3_theme
"""
import os
from zopeskel.base import var
from zopeskel.localcommands import ZopeSkelLocalTemplate

class QThemeSubTemplate(ZopeSkelLocalTemplate):
    use_cheetah = True
    parent_templates = ['qplone3_theme']

    # Flag for use template composition
    compose = None
    compodir_pref = "_compo"
    # list of 2 item tuple -
    # (compotemplate_name, compo marker), for ex.:
    compo_template_markers = []

    def template_dir(self):
        if self.compose:
            # Prepare
            self._template_dir = os.path.join( \
                self._template_dir + self.compodir_pref, \
                self.compose )

        return super(QThemeSubTemplate, self).template_dir()

    def post(self, command, output_dir, vars):
        """ Call write_files function for every subtemplate,
             - change marker name for every subtemplate,
             - set compose prop for change subtemplate path calculation
        """

        if self.compo_template_markers:
            for cname, cmarker in self.compo_template_markers:
                original_template_dir = self._template_dir
                self.compose = cname
                self.marker_name = cmarker
                self.write_files(command, output_dir, vars)
                self._template_dir = original_template_dir

        super(QThemeSubTemplate, self).post(command, output_dir, vars)

