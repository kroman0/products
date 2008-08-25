Plone Capchas

    qPloneCaptchas is simple captchas implementation for Plone, designed
    for validating human input in insecure forms. This is a standalone
    implementation with static captcha images, which does not depend on
    captchas.net services.

    Since version 1.0, the dynamic captchas option is implemented. You can
    switch captchas into dynamic mode in correspondent configlet. In this
    case, captcha images will be generated on the fly.


Supported Plone versions:

    * 2.0.x
    * 2.1.x
    * 2.5.x
    * 3.x


Dependency:

    PIL with Jpeg and FreeType support


Plugs to:

    * default Plone discussion mechanism
    * PloneFormMailer anonymous contact forms


Install:

    If qPloneCaptchas is expected to be used with PloneFormMailer please
    make sure that qPloneCaptchas is installed only after the product.
    Tested with PloneFormMailer 0.3.


Authors:

    The product is developed by Quintagroup.com team:

    * Volodymyr Cherepanyak - chervol@quintagroup.com

    * Mykola Kharechko - crchemist@quintagroup.com


Contributors:

    * Dorneles Tremea - dorneles@tremea.com


Future features:

    * Configuration of captchas images generation (shade, background, colors etc.)
