"""Definition of the Bounty Program Submission content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.configuration import zconf
from Products.validation import V_REQUIRED

# -*- Message Factory Imported Here -*-
from ploneorg.kudobounty import kudobountyMessageFactory as _

from ploneorg.kudobounty.interfaces import IBountyProgramSubmission
from ploneorg.kudobounty.config import PROJECTNAME

BountyProgramSubmissionSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.ComputedField(
        name='title',
        required=1,
        searchable=1,
        default='',
        accessor='Title',
        storage=atapi.AnnotationStorage(),
        widget=atapi.ComputedWidget(
            label=_(u'Name'),
        ),
        expression="' '.join(filter(None, [context.getFirstName(),context.getLastName()])) + " \
                   "context.getFirstName() or context.getLastName() and ', ' or '' + "\
                   "context.getOrganization()"
    ),

    atapi.ImageField(
        'image',
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        swallowResizeExceptions = zconf.swallowImageResizeExceptions.enable,
        pil_quality = zconf.pil_config.quality,
        pil_resize_algo = zconf.pil_config.resize_algo,
        max_size = zconf.ATImage.max_image_dimension,
        sizes= {'bounty': (150,100),},
        widget=atapi.ImageWidget(
            label=_(u"Image"),
            description=_(u"Image or Logo"),
        ),
        required=True,
        validators = (('isNonEmptyFile', V_REQUIRED),
                      ('checkImageMaxSize', V_REQUIRED)),
    ),

    atapi.StringField(
        'remoteUrl', # for use getRemoteUrl metadata from catalog
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"URL"),
            maxlength = '511',
        ),
        required=True,
        validators=('isURL'),
        default = "http://",
    ),

    atapi.StringField(
        'description',
        accessor='Description',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"alt text"),
        ),
    ),

    atapi.StringField(
        'firstName',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"First name"),
            description=_(u"Field description"),
        ),
    ),

    atapi.StringField(
        'lastName',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Last name"),
            description=_(u"Field description"),
        ),
    ),

    atapi.StringField(
        'organization',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Organization name"),
            description=_(u"Field description"),
        ),
    ),

    atapi.StringField(
        'email',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Email address"),
        ),
        validators=('isEmail'),
    ),

    atapi.TextField(
        'mission',
        storage=atapi.AnnotationStorage(),
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        widget=atapi.TextAreaWidget(
            label=_(u"Bounty mission"),
            description=_(u"Bounty mission trac ticket #"),
        ),
        required=True,
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

BountyProgramSubmissionSchema = schemata.finalizeATCTSchema(
    BountyProgramSubmissionSchema, moveDiscussion=False)
BountyProgramSubmissionSchema.moveField('description', after='remoteUrl')


class BountyProgramSubmission(base.ATCTContent):
    """Information for Bounty Program Submission"""
    implements(IBountyProgramSubmission)

    meta_type = "BountyProgramSubmission"
    schema = BountyProgramSubmissionSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    image = atapi.ATFieldProperty('image')
    remoteUrl = atapi.ATFieldProperty('remoteUrl')
    firstName = atapi.ATFieldProperty('firstName')
    lastName = atapi.ATFieldProperty('lastName')
    organization = atapi.ATFieldProperty('organization')
    email = atapi.ATFieldProperty('email')
    mission = atapi.ATFieldProperty('mission')

    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return base.ATCTContent.__bobo_traverse__(self, REQUEST, name)
    
atapi.registerType(BountyProgramSubmission, PROJECTNAME)
