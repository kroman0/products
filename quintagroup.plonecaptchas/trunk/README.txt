Plone Captchas
==============

Introduction
------------

quintagroup.plonecaptchas is a simple captchas implementation for Plone, designed
for validation of human input in insecure forms. This is a standalone 
implementation with static captcha images, which does not depend on captchas.net 
services.

quintagroup.plonecaptchas has dynamic captchas option implemented. You can
switch captchas into dynamic mode in the correspondent configlet. In this
case, captcha images will be generated on the fly.

quintagroup.plonecaptchas is an eggified version of qPloneCaptchas product.

Dependency
----------

PIL with Jpeg and FreeType support

Plugs to
--------

* default Plone discussion mechanism

* join form

* send to form

* forms created with PloneFromGen

To make captchas work on forms created with PloneFormGen, please use qPloneCaptchaField product:

 * Home page - http://quintagroup.com/services/plone-development/products/plone-captcha-field

 * Instruction on use - http://projects.quintagroup.com/products/wiki/qPloneCaptchaField

Requirements
------------

* Plone 3.0+ 

For earlier Plone versions use qPloneCaptchas product.

Installation
------------

See docs/INSTALL.txt for instructions.

Authors
-------

The product is developed by Quintagroup team:

* Volodymyr Cherepanyak

* Mykola Kharechko

* Vitaliy Stepanov

* Bohdan Koval

Contributors
------------

* Dorneles Tremea

Future features
---------------

* Configuration of captchas images generation (shade, background, colors etc.)

Links
-----

* Home page - http://quintagroup.com/services/plone-development/products/plone-captchas

* Screencast - http://quintagroup.com/cms/screencasts/qplonecaptchas/