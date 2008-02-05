from Products.CMFCore.utils import getToolByName
from AccessControl import ModuleSecurityInfo
import re

security = ModuleSecurityInfo('Products.qPloneSkinDump.generatingTemplate')

tags = {'default'   : '<td id="portal-columns-%s" colspan="3">\n%s\n</td>',
        'tableless' : '<div id="portal-columns-%s">\n%s\n</div>'}
div = '<div metal:use-macro="%s">Some content from macro</div>'
span = '<span tal:replace="structure python:path(\'%s\')" />'
pattern = re.compile(r"<([^< ]*)[^<]*extract_portlets\('(.*?)'\).*?>", re.DOTALL)

p_sheet_id = 'generation_properties'
p_id = 'subfolder_name'

security.declarePublic('generate')
def generate(context, skin_name, layer_name, subfolder_name):
    # add property sheet on plone site object which will store subfolder name with generated main_template.pt
    pp = getToolByName(context, 'portal_properties')
    if not p_sheet_id in pp.objectIds():
        pp.addPropertySheet(id=p_sheet_id, title=p_sheet_id)
    else:
        pp.manage_delObjects(ids=[p_sheet_id])
        pp.addPropertySheet(id=p_sheet_id, title=p_sheet_id)
    p_sheet = pp[p_sheet_id]
    if p_sheet.hasProperty(p_id):
        p_sheet._updateProperty(p_id, subfolder_name)
    else:
        p_sheet._setProperty(p_id, subfolder_name, 'string')
    ps = getToolByName(context, 'portal_skins')
    # get the most specific main_template, which is contained in current skin's layers
    paths = ps.getSkinPath(skin_name).split(',')
    for path in paths:
        if 'main_template' in ps[path].objectIds():
            break
    mt = ps[path].main_template.document_src()
    # find all slots which must be expand
    finded_slots = pattern.findall(mt)
    for tag, slot_name in finded_slots:
        # now we'll use qMultipleSlots product's extract_portlets function and create replacement string
        slots = context.extract_portlets(slot_name)
        replacement = []
        for k, v in slots:
            if v: replacement.append(div % k)
            else: replacement.append(span % k)
        replacement = '\n'.join(replacement)
        # next find the part of main_template which will be replaced
        m = pattern.search(mt)
        closing_tag = "</%s>" % tag
        start = m.start()
        end = mt[start:].find(closing_tag) + start + len(closing_tag)
        string_to_replace = mt[start:end]
        # next is needed for placing replacement in <div> or <td> tags
        if slot_name.startswith('columns'):
            outer_tag = '</div>' in string_to_replace and tags['tableless'] or tags['default']
            replacement = replacement and outer_tag % (slot_name.split('_')[1], replacement)
        mt = mt.replace(string_to_replace, replacement)
    # create template object in portal_skins
    ps[layer_name].manage_addFolder(id=subfolder_name)
    subfolder = getattr(ps[layer_name], subfolder_name)
    subfolder.manage_addProduct['PageTemplates'].manage_addPageTemplate(id='main_template', text=mt)

security.declarePublic('available')
def available(context):
    ps = getToolByName(context, 'portal_skins')
    skin_name = context.getCurrentSkinName()
    paths = ps.getSkinPath(skin_name).split(',')
    return 'qmultipleslots' in paths

security.apply(globals())