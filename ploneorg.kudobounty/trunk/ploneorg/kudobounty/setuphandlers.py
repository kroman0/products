from ploneorg.kudobounty.config import FORM_ID
from ploneorg.kudobounty.config import TOPIC_ID
from ploneorg.kudobounty.config import SUBMISSION_CONTAINER_ID

from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.context import TarballExportContext, TarballImportContext
from Products.GenericSetup.interfaces import IFilesystemExporter, IFilesystemImporter

CREATE_SCRIPT_BODY = """
portal = context.portal_url.getPortalObject()
formProcessor = portal.restrictedTraverse('@@processBountyForm')
formProcessor()
return {}
"""

def createTopic(container, logger):
    """
    Located in: /bounty-mission/index_html

    Item Type = ["Bounty Program Submission",]
    state = ['published',]

    sort_on = "creation"    
    """
    theCollection = getattr(container, TOPIC_ID, None)
    ptype = getattr(theCollection, 'portal_type', None)
    if not ptype == "Topic":
        container.invokeFactory(id=TOPIC_ID, type_name="Topic")
        theCollection = getattr(container, TOPIC_ID)
        theCollection.unmarkCreationFlag()
        theCriteria = theCollection.addCriterion('Type','ATPortalTypeCriterion')
        theCriteria.setValue(["Bounty Program Submission",])
        theCriteria = theCollection.addCriterion('review_state','ATSelectionCriterion')
        theCriteria.setValue("published")
        theCriteria = theCollection.addCriterion('created','ATSortCriterion') 
        logger.info("To '%s' added collection, which grab all " \
                    "'Bounty Program Submission' objects" % \
                    '/'.join(theCriteria.getPhysicalPath()))
    else:
        logger.info("To '%s' collection already present in the portal" \
                    % '/'.join(theCollection.getPhysicalPath())) 

def createPFGForm(context, container, logger):
    """
    """
    form = getattr(container, FORM_ID, None)
    wftool = getToolByName(container, "portal_workflow")

    if form is not None:
        # Delete form if it exist
        container.manage_delObjects(ids = FORM_ID)

    # Create new form object
    container.invokeFactory(id=FORM_ID, type_name="FormFolder",
                           title="Form of Bounty Program")
    form = getattr(container, FORM_ID)
    logger.info("To '%s' added Form Folder" % \
                '/'.join(form.getPhysicalPath()))
    # cleanup form and import data from the archive
    form.manage_delObjects(ids=form.objectIds())
    pfg_data = context.readDataFile("pfg_data.tar.gz")
    ctx = TarballImportContext(form, pfg_data)
    IFilesystemImporter(form).import_(ctx, 'structure', True)
    logger.info("Successfully imported PFG from data from archive into the form")
    # Fix importing PFG via GS bug
    #   - it adds extra indentation, wchich breaks the script.
    create_bounty_script = form["create-bounty-submission"]
    create_bounty_script.setScriptBody(CREATE_SCRIPT_BODY)
    # Update form
    form.update(**{"actionAdapter":["create-bounty-submission",],})
    form.unmarkCreationFlag()
    form.reindexObject()
    # Publish the form
    if wftool.getInfoFor(form, 'review_state') != 'published':
        wftool.doActionFor(form, 'publish')
        logger.info("'%s' PFG form successfully published" % form.Title())
    else:
        logger.info("'%s' PFG form already in 'published' state" % form.Title())

def createStructure(context, logger):
    site = context.getSite()

    subcontainer = getattr(site, SUBMISSION_CONTAINER_ID, None)
    if subcontainer is None:
        site.invokeFactory("Folder", SUBMISSION_CONTAINER_ID)
        subcontainer = getattr(site, SUBMISSION_CONTAINER_ID)
        subcontainer.update(title="Bounty Submissions container")
        logger.info("Successfully crated '%s' submissions container" \
                    "in the portal" % SUBMISSION_CONTAINER_ID)
    else:
        logger.info("To '%s' container already present in the portal" \
                    % '/'.join(subcontainer.getPhysicalPath())) 

    createTopic(subcontainer, logger)
    createPFGForm(context, subcontainer, logger)
        


def importVarious(context):
    """ Various import steps
    """
    if context.readDataFile('ploneorg_kudobounty.txt') is None:
        return
    logger = context.getLogger("ploneorg.kudobounty")
    
    createStructure(context, logger)
