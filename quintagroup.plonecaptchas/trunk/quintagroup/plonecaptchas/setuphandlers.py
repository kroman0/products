from random import randint

from quintagroup.plonecaptchas.config import CAPTCHA_KEY

def generateKey(length):
    key = ''
    for i in range(length):
        key += str(randint(0, 9))
    return key

def setupVarious(context):
    if context.readDataFile('quintagroup.plonecaptchas_various.txt') is None:
        return

    site = context.getSite()

    # set captcha key
    value = generateKey(8)
    if site.hasProperty(CAPTCHA_KEY):
        site._updateProperty(CAPTCHA_KEY, value)
    else:
        site._setProperty(CAPTCHA_KEY, value, 'string')
