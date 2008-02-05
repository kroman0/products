from cStringIO import StringIO

from PIL import Image



# Settings for member image resize quality
PIL_SCALING_ALGO = Image.ANTIALIAS
PIL_QUALITY = 88
MEMBER_IMAGE_SCALE = (75, 100)

def scale_image(image_file, max_size=MEMBER_IMAGE_SCALE,
                default_format = 'PNG'):
    """Scales an image down to at most max_size preserving aspect ratio
    from an input file

        >>> import Products.CMFPlone
        >>> import os
        >>> from StringIO import StringIO
        >>> from Products.CMFPlone.utils import scale_image
        >>> from PIL import Image

    Let's make a couple test images and see how it works (all are
    100x100), the gif is palletted mode::

        >>> plone_path = os.path.dirname(Products.CMFPlone.__file__)
        >>> pjoin = os.path.join
        >>> path = pjoin(plone_path, 'tests', 'images')
        >>> orig_jpg = open(pjoin(path, 'test.jpg'))
        >>> orig_png = open(pjoin(path, 'test.png'))
        >>> orig_gif = open(pjoin(path, 'test.gif'))

    We'll also make some evil non-images, including one which
    masquerades as a jpeg (which would trick OFS.Image)::

        >>> invalid = StringIO('<div>Evil!!!</div>')
        >>> sneaky = StringIO('\377\330<div>Evil!!!</div>')

    OK, let's get to it, first check that our bad images fail:

        >>> scale_image(invalid, (50, 50))
        Traceback (most recent call last):
        ...
        IOError: cannot identify image file
        >>> scale_image(sneaky, (50, 50))
        Traceback (most recent call last):
        ...
        IOError: cannot identify image file

    Now that that's out of the way we check on our real images to make
    sure the format and mode are preserved, that they are scaled, and that they
    return the correct mimetype::

        >>> new_jpg, mimetype = scale_image(orig_jpg, (50, 50))
        >>> img = Image.open(new_jpg)
        >>> img.size
        (50, 50)
        >>> img.format
        'JPEG'
        >>> mimetype
        'image/jpeg'

        >>> new_png, mimetype = scale_image(orig_png, (50, 50))
        >>> img = Image.open(new_png)
        >>> img.size
        (50, 50)
        >>> img.format
        'PNG'
        >>> mimetype
        'image/png'

        >>> new_gif, mimetype = scale_image(orig_gif, (50, 50))
        >>> img = Image.open(new_gif)
        >>> img.size
        (50, 50)
        >>> img.format
        'GIF'
        >>> img.mode
        'P'
        >>> mimetype
        'image/gif'

    We should also preserve the aspect ratio by scaling to the given
    width only unless told not to (we need to reset out files before
    trying again though::

        >>> orig_jpg.seek(0)
        >>> new_jpg, mimetype = scale_image(orig_jpg, (70, 100))
        >>> img = Image.open(new_jpg)
        >>> img.size
        (70, 70)

        >>> orig_jpg.seek(0)
        >>> new_jpg, mimetype = scale_image(orig_jpg, (70, 50))
        >>> img = Image.open(new_jpg)
        >>> img.size
        (50, 50)

    """
    # Make sure we have ints
    size = (int(max_size[0]), int(max_size[1]))
    # Load up the image, don't try to catch errors, we want to fail miserably
    # on invalid images
    image = Image.open(image_file)
    # When might image.format not be true?
    format = image.format
    mimetype = 'image/%s'%format.lower()
    cur_size = image.size
    # from Archetypes ImageField
    # consider image mode when scaling
    # source images can be mode '1','L,','P','RGB(A)'
    # convert to greyscale or RGBA before scaling
    # preserve palletted mode (but not pallette)
    # for palletted-only image formats, e.g. GIF
    # PNG compression is OK for RGBA thumbnails
    original_mode = image.mode
    if original_mode == '1':
        image = image.convert('L')
    elif original_mode == 'P':
        image = image.convert('RGBA')
    # Rescale in place with an method that will not alter the aspect ratio
    # and will only shrink the image not enlarge it.
    image.thumbnail(size, resample=PIL_SCALING_ALGO)
    # preserve palletted mode for GIF and PNG
    if original_mode == 'P' and format in ('GIF', 'PNG'):
        image = image.convert('P')
    # Save
    new_file = StringIO()
    image.save(new_file, format, quality=PIL_QUALITY)
    new_file.seek(0)
    # Return the file data and the new mimetype
    return new_file, mimetype

