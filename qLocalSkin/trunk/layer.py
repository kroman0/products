from zope.component import queryUtility, queryMultiAdapter

from zope.publisher.interfaces.browser import IBrowserSkinType
from zope.publisher.browser import applySkin

from adapters.interfaces import ISkinNameExtractor, IRequestPortalUrlAnnotator

def mark_layer(context, event):
    """Mark the request with a layer corresponding to the current marked object.
    """

    skin_name = None
    extractor = ISkinNameExtractor(context, None)
    if extractor is not None:
        skin_name = extractor.getSkinName()
    if skin_name is not None:
        skin = queryUtility(IBrowserSkinType, name=skin_name)
        if skin is not None:
            applySkin(event.request, skin)
            context.changeSkin(skin_name, event.request)
            annotator = IRequestPortalUrlAnnotator(event.request, None)
            if annotator is not None:
                annotator.annotate('/' + '/'.join(context.getPhysicalPath()[2:]))
