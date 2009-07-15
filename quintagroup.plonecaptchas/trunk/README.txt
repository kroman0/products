Plone Captchas
==============

Introduction
------------

quintagroup.plonecaptchas is a simple captchas implementation for Plone, designed
for validation of human input in insecure forms. This is a standalone 
implementation with static captcha images, which does not depend on captchas.net 
services.

Since version 1.0, the dynamic captchas option is implemented. You can
switch captchas into dynamic mode in the correspondent configlet. In this
case, captcha images will be generated on the fly.

Dependency
----------

PIL with Jpeg and FreeType support

Plugs to
--------

* default Plone discussion mechanism
* join form
* send to form

Requirements
------------

* Plone 3.0+ 

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

zzz
