PROJECTNAME = "qPloneComments"

GLOBALS = globals()
SKINS_DIR = "skins"
SKIN_NAME = "qplonecomments"

CONFIGLET_ID = "prefs_comments_setup_form"
CONFIGLET_NAME = "qPloneComments setup"

PROPERTIES = (('enable_approve_user_notification', 'True', 'boolean'),
              ('enable_reply_user_notification', 'True', 'boolean'),
              ('enable_rejected_user_notification', 'True', 'boolean'),
              ('enable_moderation', 'True', 'boolean'),
              ('require_email', 'False', 'boolean'),
              ('enable_anonymous_commenting', 'True', 'boolean'),
              ('enable_published_notification', 'True', 'boolean'),
              ('enable_approve_notification', 'True', 'boolean'),
              ('email_discussion_manager', '', 'string'),
              ('email_subject_prefix', '', 'string'))
