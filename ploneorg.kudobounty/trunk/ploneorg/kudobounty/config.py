"""Common configuration constants
"""

PROJECTNAME = 'ploneorg.kudobounty'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'BountyProgramSubmission': 'ploneorg.kudobounty: Add Bounty Program Submission',
}

SUBMISSION_CONTAINER_ID = "bounty-submissions"
FORM_ID = "bounty-submissions-form"
FORM_PATH = "/".join([SUBMISSION_CONTAINER_ID, FORM_ID])
TOPIC_ID = "index.html"
TOPIC_PATH = "/".join([SUBMISSION_CONTAINER_ID, TOPIC_ID])


