Plone Comments

  Plone Comments (qPloneComments) is a Plone product developed developed
  to improve the site managers and editors expirience with standard
  commenting mechanism in Plone.

Features

  * Notify admin about comment posted

  * Notify commentator about his comment aproval

  * Notify author of parent comment about new follow up added

  * Moderation of comments, approval of comments

  * Anonymous commenting

  * Added Name field to comment form, it is required for anonymous comments

  * Article author can be notified about new comment after the approval by reviewer

  * List of recent comments for more comfortable moderation

  * Configlet that allow:

    o Turning on/off Moderation

    o Turning on/off Manager notification

    o Turning on/off Editor notification

    o Turning on/off Anonymous Commenting

    o Configure admin e-mail for notifications

    o Configure notification subject

  * qPloneCaptcha integrated (needs the qPloneCaptcha to be installed)

Notes

  Comments moderation is implemented with involvement of two stage workflow.
  Comments are created in "private" state and visible only to DiscussionManager
  group of users.

  To differentiate between logged-in (registered) commentors and Anonymous
  commentors that pretend to be one person or other one, we use Boldness of
  name. The Comment author is in bold when posted by logged in member. The
  names provided when posting Anonymously are in plain text.

  Notification subject control allows to enter custom prefix to disctinct
  notifications comming from different sites.

Usage

  One of possible UseCases:

  Moderation is enabled and authors notification is turned on.

    * New comment posted in private state.

    * Notification is sent to the emails entered in Plone Comments configlet.

    * Moderator User with DiscussionManager role see the comment.

    * The comment can be deleted or published on modaration stage.

    * When comment is published notification is sent to Article Editor.

Links

  * Download releases from Sourceforge.net "Plone Comments project area":http://sf.net/projects/quintagroup

  * Get latest development version from "SVN":http://svn.quintagroup.com/products/qPloneComments/trunk

Requirements

  * Plone 3.0.x (with plone.browserlayer) or Plone 3.1.x.

Installation

   1. Unpack into the **Products** folder of your Zope instance.

   2. Install *qPloneComments* with Quick Installer.

  **Atention**: If you are using a Plone version **before** 3.1 you need to install
  "plone.browserlayer":http://pypi.python.org/pypi/plone.browserlayer (which also
  requires a "GenericSetup":http://pypi.python.org/pypi/Products.GenericSetup version
  greater than 1.4) in your Plone site. It shows up as **Local browser layer support**
  in the Plone Add-on Products Control Panel.

License

  Please find license in *LICENSE.GPL*.

Author

  The product is developed and maintained by http://quintagroup.com team.

  Authors:

    * Volodymyr Cherepanyak

    * Andriy Mylenkyy

    * Mykola Kharechko

  Contributors

    * Gerry Kirk: product translations improvement and proofreading

    * Dorneles Tremea: code cleanup and generic setup porting
