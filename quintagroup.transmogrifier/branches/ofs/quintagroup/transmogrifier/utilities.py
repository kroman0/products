from zope.interface import implements

class ImageFTI(object):
    def _constructInstance(self, container, id, *args, **kw):
        """Build a bare instance of the appropriate type.
        Does not do any security checks.
        Returns the object without calling _finishConstruction().
        """
        file, title = None, ''
        id = container.manage_addProduct['OFSP'].manage_addImage(id, file, title)
        return container.get(id, None)

    def _finishConstruction(self, obj):
        """Finish the construction of a content object.
        Set its portal_type, insert it into the workflows.
        """
        return obj

ImageFTIUtility = ImageFTI()

class FileFTI(object):
    def _constructInstance(self, container, id, *args, **kw):
        """Build a bare instance of the appropriate type.
        Does not do any security checks.
        Returns the object without calling _finishConstruction().
        """
        file, title = None, ''
        id = container.manage_addProduct['OFSP'].manage_addFile(id, file, title)
        return container.get(id, None)

    def _finishConstruction(self, obj):
        """Finish the construction of a content object.
        Set its portal_type, insert it into the workflows.
        """
        return obj

FileFTIUtility = FileFTI()
