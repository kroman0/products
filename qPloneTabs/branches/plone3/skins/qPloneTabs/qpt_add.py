## Script (Python) "qpt_add"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= idx, name, action='', id, category='portal_tabs', condition='', visible=False
##title=
##

from Products.CMFCore.utils import getToolByName

if action:
    from Products.qPloneTabs.utils import processUrl
    action = processUrl(context, str(action))
if visible:
    checked = """checked="checked" """
    liClass = ""
    visible = True
else:
    checked = ""
    liClass = "invisible"
    visible = False
params = {'id':id, 'name':name, 'action':action, 'condition':condition,
          'permission':'View', 'category':category, 'visible':visible}
act_tool = getToolByName(context, 'portal_actions')
act_tool.addAction(**params)
params.update({'idx':idx, 'abs_url':context.portal_url(), 'checked':checked, 'class':liClass})
return """
<li id="tabslist_%(id)s" class="%(class)s">
  <img class="drag-handle" src="drag.gif" alt="" height="11" width="25">
  <div class="bridge"><input class="visibility" value="1" name="i%(idx)s_visibility" %(checked)s type="checkbox" title="visibility"></div>
  <a class="delete" href="#">Delete</a>
  <span class="url-helper">%(action)s</span>
  <span class="tab-title">%(name)s</span>
  <form class="editform" method="post" action="%(abs_url)s/prefs_tabs_form" name="f%(idx)s">
    <input type="hidden" name="idx" value="%(idx)s" />
      <dl>
        <dt><label>Name</label></dt>
        <dd><input type="text"     value="%(name)s"      name="i%(idx)s_name"                /></dd>
      </dl>
      <dl class="collapseAdvanced collapsedBlock">
        <dt class="headerAdvanced">Advanced</dt>
        <dd class="contentAdvanced">
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
    <div>
      <input type="submit" class="editsave"   value="Save"   />
      <input type="submit" class="editcancel" value="Cancel" />
    </div>
  </form>
</li>\n""" % params