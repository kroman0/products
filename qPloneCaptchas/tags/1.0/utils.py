import os
from string import atoi
import md5
from random import randint
from Products.qPloneCaptchas.data import basic_english
from Products.qPloneCaptchas.config import havePIL, CAPTCHAS_COUNT
from DateTime import DateTime
import re
try:
    import Crypto.Cipher.DES as Crypto
except:
    import Crypto

def encrypt1(s):
    return md5.new(s).hexdigest().upper()

def gen_captcha(text, fnt_sz, fmt='JPEG'):
    """Generate a captcha image"""
    import ImageFile
    import Image
    import ImageFont
    import ImageDraw
    import ImageFilter
    from PIL import ImageFile as pyImageFile
    import sys
    sys.modules['ImageFile'] = pyImageFile
    from cStringIO import StringIO
    outFile = StringIO()

    DATA_PATH = os.path.abspath(os.path.dirname(__file__)) + '/data'
    FONT_PATH = DATA_PATH + '/fonts'

    # randomly select the foreground color
    fgcolor = randint(0x000000,0x000fff)
    # make the background color the opposite of fgcolor
    bgcolor = fgcolor ^ 0xffffff
    # create a font object
    import sys
    font = ImageFont.truetype(FONT_PATH+'/vera/Vera.ttf', fnt_sz)
    # determine dimensions of the text
    dim = font.getsize(text)
    # create a new image slightly larger that the text
    im = Image.new('RGB', (dim[0]+5,dim[1]+5), bgcolor)
    d = ImageDraw.Draw(im)
    x, y = im.size
    r = randint
    # draw 100 random colored boxes on the background

    for num in range(50):
        d.rectangle((r(0,x),r(0,y),r(0,x),r(0,y)),fill=r(0xfff000,0xffffff))

    # add the text to the image
    d.text((3,3), text, font=font, fill=fgcolor)
    
    for num in range(10):
        d.line([(r(0,x), r(0,y)), (r(0,x), r(0,y))], fill=r(0xf0f000, 0xffffff))

    im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)

    # save the image to a file
    im.save(outFile, format=fmt)
    outFile.seek(0)
    src = outFile.read()
    size = len(src)
    sys.modules['ImageFile'] = ImageFile
    return {'src':src, 'size':size}


def getWord(index):
    words = basic_english.words.split()
    return words[index]

def getIndex(word):
    words = basic_english.words.split()
    try:
        res = words.index(word)
    except ValueError:
        res = getLen()+1
    return res

def getCaptchasCount(havePIL):
    def getLen():
        return len(basic_english.words.split())
    return havePIL and getLen() or CAPTCHAS_COUNT

def formKey(num):
    def normalize(s):
        return (not len(s)%8 and s) or normalize(s+str(randint(0, 9)))

    return normalize('%s_%i_'%(str(DateTime().timeTime()), num))

def encrypt(key, s):
    return toHex(Crypto.new(key).encrypt(s))

def decrypt(key, s):
    return Crypto.new(key).decrypt(toStr(s))

def parseKey(s):
    ps = re.match('^(.+?)_(.+?)_', s)
    return {'date': ps.group(1), 'key':ps.group(2)}

"""
def addExpiredKey(context, key):
    context.portal_captchas.new(key)
"""

def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)

    return reduce(lambda x,y:x+y, lst)

def toStr(s):
    return s and chr(atoi(s[:2], base=16)) + toStr(s[2:]) or ''
