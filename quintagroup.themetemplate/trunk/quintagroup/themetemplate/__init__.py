#
import os
from paste.script import pluginlib

from quintagroup.themetemplate.qplone3_theme import qPlone3Theme

def getEggInfo(output_dir):
    """ Return path to egg info directory, raise error if not found.
    """
    egg_info = pluginlib.find_egg_info_dir(output_dir)
    assert egg_info is not None, "egg_info directory must present for the package"

    return egg_info


def getThemeVarsFP(egg_info):
    """ Return file system path to theme vars configurations
    """
    return os.path.join(egg_info, '..', 'theme_vars.cfg')
