from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from ploneorg.kudobounty import kudobountyMessageFactory as _


class IBountyProgramSubmission(Interface):
    """Information for Bounty Program Submission"""

    # -*- schema definition goes here -*-
    mission = schema.Text(
        title=_(u"Bounty mission"),
        required=True,
        description=_(u"Bounty mission trac ticket #"),
    )
#
    email = schema.TextLine(
        title=_(u"Email address"),
        required=False,
    )
#
    organization = schema.TextLine(
        title=_(u"Organization name"),
        required=False,
    )
#
    lastName = schema.TextLine(
        title=_(u"Last name"),
        required=False,
    )
#
    firstName = schema.TextLine(
        title=_(u"First name"),
        required=False,
    )
#
    # altText = schema.TextLine(
    #     title=_(u"alt text"),
    #     required=False,
    #     description=_(u"Field description"),
    # )
#
    remoteUrl = schema.TextLine(
        title=_(u"URL"),
        required=True,
    )
#
    image = schema.Bytes(
        title=_(u"Image"),
        required=True,
        description=_(u"Image or Logo"),
    )
#
