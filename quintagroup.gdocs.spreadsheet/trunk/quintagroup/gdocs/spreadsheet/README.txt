Introduction
============

This is a full-blown functional test. The emphasis here is on testing what
the user may input and see, and the system is largely tested as a black box.
We use PloneTestCase to set up this test as well, so we have a full Plone site
to play with. We *can* inspect the state of the portal, e.g. using 
self.portal and self.folder, but it is often frowned upon since you are not
treating the system as a black box. Also, if you, for example, log in or set
roles using calls like self.setRoles(), these are not reflected in the test
browser, which runs as a separate session.

Being a doctest, we can tell a story here.

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the 
documentation, though, is in the underlying zope.testbrower package.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> self.portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from Products.PloneTestCase.setup import portal_owner, default_password

    >>> browser.open(portal_url)

We have the login portlet, so let's use that.

    >>> browser.getLink('Log in').click()
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.

We then test that we are still on the portal front page:

    >>> browser.url == portal_url
    True

And we ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True


-*- extra stuff goes here -*-
The GSpreadsheet content type
===============================

In this section we are tesing the GSpreadsheet content type by performing
basic operations like adding, updadating and deleting GSpreadsheet content
items.

Adding a new GSpreadsheet content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'GSpreadsheet' and click the 'Add' button to get to the add form.

    >>> browser.getControl('GSpreadsheet').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'GSpreadsheet' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'GSpreadsheet Sample'
    >>> browser.getControl(name='spreadsheet_id').value = 'sp_id1'
    >>> browser.getControl(name='worksheet_id').value = 'od6'
    >>> browser.getControl(name='order_columns.column_key:records',index=0).value
    []
    >>> browser.getControl(name='order_columns.column_title:records', index=0).value
    ''
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'GSpreadsheet' content item to the portal.

Updating an existing GSpreadsheet content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New GSpreadsheet Sample'
    >>> browser.getControl(name='spreadsheet_id').value = 'id1'
    >>> browser.getControl(name='worksheet_id').value = 'od6'
    >>> browser.getControl(name='order_columns.orderindex_:records',index=0).value = '1'    
    >>> browser.getControl(name='order_columns.column_key:records',index=0).value = ['col1']
    >>> browser.getControl(name='order_columns.column_title:records', index=0).value = 'Title 1'
    >>> browser.getControl('Save').click()
    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='order_columns.orderindex_:records',index=1).value = '2'    
    >>> browser.getControl(name='order_columns.column_key:records',index=1).value = ['col2']
    >>> browser.getControl(name='order_columns.column_title:records', index=1).value = 'Title 2'
    >>> browser.getControl('Save').click()
    
We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New GSpreadsheet Sample' in browser.contents
    True
    >>> browser.contents
    '...<table id="sshwsh"><tr><th>Title 1</th><th>Title 2</th></tr><tr><td>11</td><td>12</td></tr>\n<tr><td>21</td><td>22</td></tr>\n<tr><td>31</td><td>32</td></tr>\n<tr><td>41</td><td>42</td></tr>\n<tr><td>51</td><td>52</td></tr>\n</table>...'

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='order_columns.orderindex_:records',index=1).value = '2'    
    >>> browser.getControl(name='order_columns.column_key:records',index=1).value = ['col3']
    >>> browser.getControl(name='order_columns.column_title:records', index=1).value = 'Title 3'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> browser.contents
    '...<table id="sshwsh"><tr><th>Title 1</th><th>Title 3</th></tr><tr><td>11</td><td>13</td></tr>\n<tr><td>21</td><td>23</td></tr>\n<tr><td>31</td><td>33</td></tr>\n<tr><td>41</td><td>43</td></tr>\n<tr><td>51</td><td>53</td></tr>\n</table>...'

Removing a/an GSpreadsheet content item
--------------------------------

If we go to the home page, we can see a tab with the 'New GSpreadsheet
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New GSpreadsheet Sample' in browser.contents
    True

Now we are going to delete the 'New GSpreadsheet Sample' object. First we
go to the contents tab and select the 'New GSpreadsheet Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New GSpreadsheet Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New GSpreadsheet
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New GSpreadsheet Sample' in browser.contents
    False

Adding a new GSpreadsheet content item as contributor
------------------------------------------------

Not only site managers are allowed to add GSpreadsheet content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getLink('Log in').click()
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'GSpreadsheet' and click the 'Add' button to get to the add form.

    >>> browser.getControl('GSpreadsheet').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'GSpreadsheet' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'GSpreadsheet Sample'
    >>> browser.getControl(name='spreadsheet_id').value = 'sp_id1'
    >>> browser.getControl(name='worksheet_id').value = 'od6'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new GSpreadsheet content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getLink('Log in').click()
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)
