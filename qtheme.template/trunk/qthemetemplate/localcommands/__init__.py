"""
Local templates for the qplone3_theme
"""
import os
from zopeskel.base import var
from zopeskel.localcommands import ZopeSkelLocalTemplate

class QThemeSubTemplate(ZopeSkelLocalTemplate):
    use_cheetah = True
    parent_templates = ['qplone3_theme']

