## Script (Python) "qpt_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= idx, num
##title=
##

req = context.REQUEST

fields = ['name', 'action', 'id', 'condition']
params = {'self':context,'num':num}
for item in fields:
    params[item] = str(req.get('i'+idx+'_'+item, None))

from Products.qPloneTabs.utils import editAction
editAction(**params)

params.update({'abs_url':context.portal_url(),'idx':idx})
return """
  <img class="drag-handle" src="drag.gif" alt="" height="11" width="25">
  <a class="delete" href="#">Delete</a>
  <span>%(name)s</span>
  <form class="editform" method="post" action="%(abs_url)s/prefs_tabs_form" name="f%(idx)s">
    <input type="hidden" name="idx" value="%(idx)s" />
    <fieldset>
      <legend>Edit '%(name)s' Action</legend>
      <dl>
        <dt><label>Name</label></dt>
        <dd><input type="text"     value="%(name)s"      name="i%(idx)s_name"                /></dd>
      </dl>
      <dl class="collapsible collapsedBlockCollapsible">
        <dt class="collapsibleHeader">Advanced</dt>
        <dd class="collapsibleContent">
          <dl>
            <dt><label>URL (Expression)</label></dt>
            <dd><input type="text" value="%(action)s"    name="i%(idx)s_action"    size="30" /></dd>
          </dl>
          <dl>
            <dt><label>Id</label></dt>
            <dd><input type="text" value="%(id)s"        name="i%(idx)s_id"                  /></dd>
          </dl>
          <dl>
            <dt><label>Condition (Expression)</label></dt>
            <dd><input type="text" value="%(condition)s" name="i%(idx)s_condition" size="30" /></dd>
          </dl>
          <div class="visualClear"><!-- --></div>
        </dd>
      </dl>
    </fieldset>
    <div>
      <input type="submit" class="editsave"   value="Save"   />
      <input type="submit" class="editcancel" value="Cancel" />
    </div>
  </form> """ % params