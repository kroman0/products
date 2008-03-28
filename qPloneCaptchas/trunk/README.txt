Plone Capchas

    qPloneCaptchas is simple captchas implementation for Plone, designed for validation 
    human input in insecure forms. This is standalone implementation with static captcha
    images, which does not depend on captchas.net services.

    Starting from version 1.0 dynamic captchas option implemented. You can switch 
    captchas into dynamic mode in correspondent configlet. In this case captcha images 
    will be generated on the fly.

Supported Plone versions:

    * 2.0.x
    * 2.1.x
    * 2.5.x
    * 3.0.x

Dependency:

    PIL with Jpeg and FreeType support

Plugs to:

    * default Plone discussion mechanism
    * PloneFormMailer anonymous contact forms


Install:

    If qPloneCaptchas is expected to be used with PloneFormMailer please make sure 
    that qPloneCaptchas installed only after the product. Tested with PloneFormMailer 0.3.


The product is developed by Quintagroup.com team.

    Volodymyr Cherepanyak - chervol@quintagroup.com
    Mykola Kharechko - crchemist@quintagroup.com

Future features:

    * Configuration of captchas images generation (shade, background, colors etc.)
