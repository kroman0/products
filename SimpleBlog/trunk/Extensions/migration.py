import sys
from Products.CMFCore.utils import getToolByName
import transaction, traceback

processed = []
brakes = []

def clean(blog, id):
    if hasattr(blog,id):
        delattr(blog,id)
    if blog.__dict__.has_key(id):
        del blog.__dict__[id]

def migrate2Btree(migrated_ob):
    global processed, brakes
    
    try:
      migrated_ob._initBTrees()
      obs = list(migrated_ob._objects)
      for o in obs:
          if o['meta_type']=='BlogFolder':
              oo=getattr(migrated_ob, o['id'], None)
              oo._initBTrees()
      while obs:
          ob_data = obs.pop()
          ob_id, ob_meta = map(lambda i:ob_data[i], ['id','meta_type'])
          object = getattr(migrated_ob, ob_id, None)
          clean(migrated_ob, ob_id)
          if object is not None:
              if object.meta_type == 'BlogFolder':
                  migrate2Btree(object)
              migrated_ob._setOb(ob_id, object)
              be = migrated_ob._getOb(ob_id,None)
              if be is None:
                  raise Exception("Not set '%s' object on '%s' blog" % (ob_id, blog.getId()))
              be._p_changed = 1
              be.reindexObject()
          else:
              raise str("%s - not exist in %s" % (ob_id, self.blog.absolute_url()))
          processed.append(ob_id)
      migrated_ob._objects = ()
      migrated_ob._p_changed = 1
      migrated_ob.reindexObject()
    except:
      err_type, err_val, traces = sys.exc_info()
      brakes.append({'url':migrated_ob.absolute_url(), "err_type":str(err_type), "err_val":str(err_val),\
                     'traces':'\n'.join(traceback.format_exception(err_type, err_val, traces))})
    return processed, brakes

def migrateBlogs(self):
    """ Migration all portal's blogs to BTreeFoolder base. """
    global processed, brakes
    
    res = ""
    catalog = getToolByName(self, 'portal_catalog')
    
    # add 'EntryCategory' to portal_catalog Metadata.
    # Update cataloged object perform on 2nd migration step
    if not 'EntryCategory' in catalog._catalog.names:
        catalog.addColumn('EntryCategory')

    # migrate old-fashion blog to btree-based
    blogs = [b.getObject() for b in catalog(portal_type="Blog")]
    for blog in blogs:
        p,b = migrate2Btree(blog)
        processed.extend(p)
        brakes.extend(b)
        
    res += 'processed: %d blogs with %d objects, brakes - %d objects.' % (len(blogs),len(processed),len(brakes))
    res += "%s\n\n%s\n\n%s" % (str(blogs),str(processed),str(brakes)) 
    
    return res
