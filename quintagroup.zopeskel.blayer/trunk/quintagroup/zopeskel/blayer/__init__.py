from string import capitalize
from zopeskel.localcommands.archetype import ArchetypeSubTemplate

class BrowserLayer(ArchetypeSubTemplate):
    """
    A Browser Layer Archetype subtemplate skeleton
    """

    _template_dir = 'templates/browserlayer'
    summary = "A browser layer"

    def pre(self, command, output_dir, vars):
        vars['layer_interface'] = "I" + ''.join(map(capitalize, vars['package_dotted_name'].split('.')))


