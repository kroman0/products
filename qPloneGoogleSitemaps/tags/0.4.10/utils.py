from urllib2 import urlopen
from urllib  import quote as urlquote
from Products.CMFCore.utils import getToolByName
import re
import Products.qPloneGoogleSitemaps.config as config
from OFS.ObjectManager import BadRequestException
def ping_google(url):
    """Ping sitemap to Google"""
    sitemap_url = urlquote(url + "/google-sitemaps")
    g = urlopen('http://www.google.com/webmasters/sitemaps/ping?sitemap='+sitemap_url)
    
    result = g.read()
    g.close()
    return 0

def searchAndReplace(string, what, with, options):
    """Emulate sed command s/"""
    res = re.sub(what,with,string)
    return res

OPERATORS = {
     's': searchAndReplace,
     }

def applyOperations(objects, operations):
    """Parse Operations """
    parse = re.compile('(.*?)/(.*|.*?[^\\\])/(.*|.*?[^\\\])/(.*)')
    operations=[parse.match(op).groups() for op in operations]
    result={}
    for ob in objects:
        url = ob.getURL()
        for operator, what, with, options in operations:
            url = OPERATORS[operator](url, what, with, options)
        #TODO: Remove or replace following condition
        #it is senseless in the case we need intelligent
        #result set. Better condition would be to place
        #freshest brain into result
        if url in result.keys():
            continue
        #TODO: replace brain with only data necessary to 
        #generate sitemap
        result[url]=ob
    return result

def additionalURLs(self):
    """Add URLs to sitemap that arn't objects"""
    res = []
    plone_home = getToolByName(self, 'portal_url').getPortalObject().absolute_url()
    root = self.getPhysicalRoot().absolute_url()

    props = getToolByName(self,'portal_properties')
    try:
        URLs = props.googlesitemap_properties.urls
    except AttributeError:
        URLs = []

    add_zope = re.compile('^/')
    add_plone= re.compile('^[^http://|https://|\\\]')
    for url in URLs:
        if add_zope.match(url):
            res.append(root+url)
        elif add_plone.match(url):
            res.append(plone_home+'/'+url)
        else:
            res.append(url)
    return res

"""workflows & co"""
def getWorkflowTransitions(self,workflow_id):
    pw = getToolByName(self,'portal_workflow')
    wf = pw.getWorkflowById(workflow_id)
    if not wf:
        return None
    return wf.transitions.values()

def setWorkflowTransitions(self,transitions):
    """set workflow transitions properties"""
    portal_workflow = getToolByName(self, 'portal_workflow')
    transmap = {}
    for key in transitions:
        if key.find('#')>0:
            ids = key.split('#')
            wfid = ids[0]
            if not wfid in transmap.keys():
                transmap[wfid]=[]
            transmap[wfid].append(ids[1])
    for wfid in transmap.keys():
        workflow = portal_workflow.getWorkflowById(wfid)
        if config.ping_googlesitemap not in workflow.scripts.objectIds():
            workflow.scripts.manage_addProduct['ExternalMethod'].manage_addExternalMethod(config.ping_googlesitemap, 'Ping sitemap', 'qPloneGoogleSitemaps.ping_googlesitemap', config.ping_googlesitemap)
        transitions_set = transmap[wfid]
        for transition in workflow.transitions.values():
            trid = transition.id
            tras = transition.after_script_name
            if (tras == '') and (trid in transitions_set):
                #set
                after_script = config.ping_googlesitemap
            elif (tras == config.ping_googlesitemap) and not (trid in transitions_set):
                #reset
                after_script = ''
            else:
                #avoid properties set
                continue
            transition.setProperties(title=transition.title,
                                     new_state_id=transition.new_state_id,
                                     after_script_name=after_script,
                                     actbox_name=transition.actbox_name)

