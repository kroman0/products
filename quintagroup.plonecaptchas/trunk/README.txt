Plone Captchas
==============

quintagroup.plonecaptchas is a simple captchas implementation for Plone, designed
for validation of human input in insecure forms. This is a standalone 
implementation with static captcha images, which does not depend on captchas.net 
services.

quintagroup.plonecaptchas adds captcha support to Plone, it works together with 
quintagroup.captcha.core package. With these products installed captchas will be 
added to Plone's 'Send this', 'Contact Us' (/contact-info) forms, and Plone's default
discussion mechanism: 'Add Comment' and 'Reply forms'.

quintagroup.plonecaptchas does not automatically plug to Plone's default registration
(/join_form). You can make captcha plug to Plone's Join form via Zope Management Interface.
Instructions here: http://projects.quintagroup.com/products/wiki/quintagroup.captcha#JoinForm 

Requirements
------------

* Plone 3.0 and above 

For earlier Plone versions - use 1.3.4 version of qPloneCaptchas product for use on forms
created with PloneFormMailer product.

Dependencies
------------

* quintagroup.captcha.core
* PIL with Jpeg and FreeType support

Plone Captchas on PloneFormGen forms 
------------------------------------

To make captchas work on forms created with PloneFormGen, please use 'quintagroup.pfg.captcha' product:

* Plone Captcha Field home page - http://quintagroup.com/services/plone-development/products/plone-captcha-field

* Instruction on use - http://projects.quintagroup.com/products/wiki/quintagroup.captcha#quintagroup.pfg.captcha

Installation
------------

See docs/INSTALL.txt for instructions.

Note: If Plone Captchas is expected to be used with Plone Comments http://quintagroup.com/services/plone-development/products/plone-comments,
for proper behavior you have to install Plone Captchas first, and then Plone Comments.

Authors
-------

The product was developed by Quintagroup team:

* Andriy Mylenkyi 

* Volodymyr Cherepanyak

* Mykola Kharechko

* Vitaliy Stepanov

* Bohdan Koval

Contributors
------------

* Dorneles Tremea

Links
-----

* Plone Captchas home page - http://quintagroup.com/services/plone-development/products/plone-captchas

* Plone Captchas Screencasts - http://quintagroup.com/cms/screencasts/qplonecaptchas
