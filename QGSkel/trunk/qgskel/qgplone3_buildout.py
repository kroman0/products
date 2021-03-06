import copy
from zopeskel import abstract_buildout
from zopeskel.base import var, EASY, EXPERT
from zopeskel.plone3_buildout import Plone3Buildout
from zopeskel.vars import BoundedIntVar

VAR_HTTP_BE1 = BoundedIntVar(
    'http_port_be1',
    title='Backend1 HTTP Port',
    description="Port that first Backend server will be serving. "\
                "Other backend' ports increments by 1 from this one.",
    default='20001',
    modes=(EXPERT,EASY),
    page='Main',
    help="""
This options lets you select the port # that Zope will use for serving
HTTP on backnd ZEO clients.
""",
    min=10000,
    max=65535,
    )

class QGPlone3Buildout(Plone3Buildout):
    _template_dir = 'templates/qgplone3_buildout'
    summary = "QG Buildout for Plone 3 projects"
    required_templates = []
    use_cheetah = True

    vars = []
    vars = copy.deepcopy(abstract_buildout.AbstractBuildout.vars)
    vars.extend(
           [ abstract_buildout.VAR_PLONEVER,
             abstract_buildout.VAR_Z2_INSTALL,
             abstract_buildout.VAR_PLONE_PRODUCTS,
             abstract_buildout.VAR_ZOPE_USER,
             abstract_buildout.VAR_ZOPE_PASSWD,
             abstract_buildout.VAR_HTTP,
             VAR_HTTP_BE1
        ]
    )

    def pre(self, command, output_dir, vars):
        vars['oldplone'] = vars['plone_version'].startswith("3.0") or \
                           vars['plone_version'].startswith("3.1")
        vars['veryoldplone'] = vars['plone_version'].startswith("2.")
        if vars['veryoldplone']:
            vars['zope2_version'] = "2.9.12"
        vars['newplone'] = not vars['veryoldplone'] and not vars['oldplone']
        vars['http_port_devel'] = int(vars['http_port']) + 10
        super(QGPlone3Buildout, self).pre(command, output_dir, vars)