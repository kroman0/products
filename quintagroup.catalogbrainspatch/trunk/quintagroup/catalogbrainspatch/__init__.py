import Products.ZCatalog.Catalog as MC
from Products.ZCatalog.CatalogBrains import AbstractCatalogBrain

oldUseBrains = MC.Catalog.useBrains
MC.registry_brains = []

def useBrains(self, brains):
    """ Sets up the Catalog to return an object (ala ZTables) that
    is created on the fly from the tuple stored in the self.data
    Btree.
    """
    scopy = self.schema.copy()
    scopy['data_record_id_']=len(self.schema.keys())
    scopy['data_record_score_']=len(self.schema.keys())+1
    scopy['data_record_normalized_score_']=len(self.schema.keys())+2

    br = [b for b in MC.registry_brains if b[0] is brains]
    if br:
        mybrains = br[0][1]
    else:
        class mybrains(AbstractCatalogBrain, brains):
            pass
        MC.registry_brains.append((brains, mybrains))

    mybrains.__record_schema__ = scopy
    self._v_brains = brains
    self._v_result_class = mybrains

MC.Catalog.useBrains = useBrains
