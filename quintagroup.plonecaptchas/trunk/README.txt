Plone Capchas
=============

Introduction
------------

quintagroup.plonecaptchas is simple captchas implementation for Plone, designed
for validating human input in insecure forms. This is a standalone 
implementation with static captcha images, which does not depend on captchas.net 
services.

Since version 1.0, the dynamic captchas option is implemented. You can
switch captchas into dynamic mode in correspondent configlet. In this
case, captcha images will be generated on the fly.

Dependency
----------

PIL with Jpeg and FreeType support


Plugs to
--------

* default Plone discussion mechanism
* join form
* send to form

Install
-------

Install quintagroup.plonecaptchas with QuickInstaller.

Authors
-------

The product is developed by Quintagroup_ team:

* `Volodymyr Cherepanyak`_
* `Mykola Kharechko`_
* `Vitaliy Stepanov`_
* `Bohdan Koval`_

Contributors
------------

* `Dorneles Tremea`_

Future features
---------------

* Configuration of captchas images generation (shade, background, colors etc.)

.. _Quintagroup: http://quintagroup.com/
.. _Volodymyr Cherepanyak: mailto:chervol@quintagroup.com
.. _Mykola Kharechko: mailto:crchemist@quintagroup.com
.. _Vitaliy Stepanov: mailto:liebster@quintagroup.com
.. _Bohdan Koval: mailto:koval@quintagroup.com
.. _Dorneles Tremea: mailto:dorneles@tremea.com
