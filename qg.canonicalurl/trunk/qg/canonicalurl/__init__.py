#
from config import DOES_PATCH_TRAVERSABLE

if DOES_PATCH_TRAVERSABLE:
    from OFS.Traversable import Traversable
    from Acquisition import aq_inner, aq_parent
    from interfaces import ICanonicalURL, ICanonicalURLRoot

    def getCanonicalURL(self):
        ob = self
        while not ICanonicalURLRoot.providedBy(ob):
            try:
                ob = aq_parent(aq_inner(ob))
            except:
                return self.absolute_url()

        curl = ICanonicalURL(ob).getCanonicalURL()
        rel_path = self.absolute_url(1)[len(ob.absolute_url(1)):]
        return curl + rel_path

    #Traversable.security.declarePublic('getCanonicalURL')
    Traversable.getCanonicalURL = getCanonicalURL
