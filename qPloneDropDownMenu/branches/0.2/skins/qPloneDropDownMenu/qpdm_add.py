## Script (Python) "qpdm_add"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= submenu_path, title, url='', num
##title=
##

from Products.CMFCore.utils import getToolByName

menu_tool = getToolByName(context, 'portal_dropdownmenu')
menu_tool.manage_addMenuItem(submenu_path, title, url)

params = {'submenu_path':submenu_path, 'title':title, 'url':url, 'num':num, 'portal_url':context.portal_url()}

return """
<li id="tabslist_%(title)s">
    <div class="deleteHover">
        <input name="submenu_path" value="%(submenu_path)s/%(num)s" type="hidden">
        <img src="./images/live_tree_transparent_pixel.gif" alt="&gt;" class="item_icon collapsed_icon">
        <img class="drag-handle" src="./images/drag.gif" alt="" height="11" width="25">
        <span>%(title)s</span>
        <a class="delete" href="#">Delete</a>
        <div class="reorder-controls"><a href="#" class="reorder">Reorder</a></div>
        <div class="sort-controls"><a href="#" class="save">Save</a> | <a href="#" class="cancel">Cancel</a></div>
        <form class="editform" method="post" action="%(portal_url)s/prefs_dropdownmenu_edit_form" name="f%(num)s">
            <input name="idx" value="%(num)s" type="hidden">
            <dl>
              <dt><label>Name</label></dt>
              <dd><input value="%(title)s" name="i%(num)s_title" type="text"></dd>
            </dl>
            <dl>
              <dt><label>URL</label></dt>
              <dd><input value="%(url)s" name="i%(title)s_url" size="30" type="text"></dd>

            </dl>
            <div>
              <input class="editsave" value="Save" type="submit">
              <input class="editcancel" value="Cancel" type="submit">
            </div>
        </form>
    </div>
    <div class="sub-items">
      <ul class="tabslist hideLevel">
        <li class="addItem">
          <form class="addform" method="post" action="%(portal_url)s/prefs_dropdownmenu_edit_form">
            <input name="submenu_path" value="%(submenu_path)s/%(num)s" type="hidden">
            <dl class="field-title"><dt><label>Name</label></dt>
              <dd><img src="./images/live_tree_transparent_pixel.gif" alt="&gt;" class="item_icon">
                  <input class="acttitle" value="" name="title" type="text"></dd></dl>
            <dl class="field-url"><dt><label>URL</label></dt>
              <dd><input class="acturl" value="" size="30" name="url" type="text"></dd></dl>
            <div class="add-controls">
              <input class="buttonadd" value="Add" type="submit">
              <input class="buttoncancel" value="Cancel" type="submit">
            </div>
          </form>
        </li>
      </ul>
    </div>
</li>\n""" % params