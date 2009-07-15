Plone Capchas
=============

qPloneCaptchas is simple captchas implementation for Plone, designed
for validation of human input in insecure forms. This is a standalone
implementation with static captcha images, which does not depend on
captchas.net services.

Since version 1.0, the dynamic captchas option is implemented. You can
switch captchas into dynamic mode in the correspondent configlet. In this
case, captcha images will be generated on the fly.

Supported Plone versions:
-------------------------

* 2.0.x

* 2.1.x

* 2.5.x

* 3.0.x - 3.1.7

For Plone version 3.0 and above we recommend you to use eggified package of this 
product - quintagroup.plonecaptchas starting from 2.0 version.

Dependency:
-----------

PIL with Jpeg and FreeType support

Plugs to:
---------

* default Plone discussion mechanism

* PloneFormMailer anonymous contact forms

Installation:
-------------

* Put qPloneCaptchas product folder into the Product fodler of your instance

* Restart Zope

* Install qPloneCaptchas in Plone with Quickinstaller

If qPloneCaptchas is expected to be used with PloneFormMailer, please
make sure that qPloneCaptchas is installed only after PloneFormMailer product.
Tested with PloneFormMailer 0.3.

Authors:
--------

The product is developed by Quintagroup.com team:

* Volodymyr Cherepanyak

* Mykola Kharechko

* Vitaliy Stepanov

* Bohdan Koval

Contributors:
-------------

* Dorneles Tremea

Future features:
----------------

* Configuration of captchas images generation (shade, background, colors etc.)

Links
-----

* home page - http://quintagroup.com/services/plone-development/products/plone-captchas

* screencast - http://quintagroup.com/cms/screencasts/qplonecaptchas/