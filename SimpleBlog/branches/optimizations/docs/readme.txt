Tip: read this document in ZMI/Products/SimpleBlog/README or in another stx aware reader.

What is SimpleBlog?

SimpleBlog is an easy to use Plone based weblog application. It has no fancy blogger-api/backlink 
stuff etc. because most of them just s.ck. but it does supports categories. Writing entries is done from inside Plone.

SimpleBlog comes with three new portal types: Blog, BlogFolder and BlogEntry:

Blog -- Folderish object that is the container for the BlogEntries and the front-page of the weblog.

BlogEntry -- Entry object inside the weblog.

BlogFolder -- Folder that can only exist inside the Blog container. The folder allows you to organize the BlogEntries in any way you like.

Getting started

    After you have set the permissions correctly in ZMI (see install.txt) you can go to any folder that you have
permissions for and add a Blog from any of the dropdown lists. You will be given a form where you can
provide the necessary information to create a new Blog:

    * **Short Name**, **Title**, **Description** will speak for themselves.
    
    * **BlogEntries to display** defines how many items should be visible on the Blog's front-page.

    * **Possible Categories** is a list of categories that can be used inside 
BlogEntries (one category per line). More about categories later.

After you have created the Blog, you can adjust its Display settings from the Display menu in Plone. Currently
there are 3 different display settings. Besides these settings, there is also a stylesheet in product's skin
that you can customize at will.

After you have created the Blog, you can start creating BlogEntries. 
Choose BlogEntry from the Add items list and fill in the form:

    * **Short Name**, **Title**, **Description**, **Body** will speak for themselves. **Note** when you 
use the Upload a file field, be aware that it will replace the current content!!

    * **Cross-post in** here  you can pick another blog in the portal where this entry will also
be shown. 

   * **Always on top** Controls if the Entry, when published is always shown first. This can be
handy for announcements etc.

    * **Categories** Select one or more categories from the list to classify 
the BlogEntry. 

    * **Related items** point to other content in your portal to indicate them as related.
    
    * **Allow Discussion on this item** control whether people can comment on this entry.
    

After the BlogEntry is saved, it will be in the 'draft' workflow state and is only visible by the owner and the manager (by default).
So, in order to make it appear on the Blog's front-page, it must be set in the 'published' state. The Blog will search and 
display the BlogEntries that have this state (this state is defined in the simpleblog_tool in ZMI and in the configlet in 
Plone setup). When putting the BlogEntry in the published state, you can also choose
to give it an effective date somewhere in the future. SimpleBlog uses the standard way of publishing content.

Inside the Blog you can create BlogFolders. These are a bit similar to the Blog itself in that it has roughly the
same view but this time it only shows the Entries that are stored inside the BlogFolder (and subfolders). BlogFolders are there
for your convenience, to organize or archive Entries in any way you want and to have additional categories (see below).

Categories

    SimpleBlog can use categories to classify BlogEntries. When you edit and configure
the Blog object, you can provide it with a list of categories that will 
present itself as a multi-selection list when you edit/create a BlogEntry. 
Next to that, BlogFolders can define additional categories. 
In BlogEntries created inside the BlogFolder, a selection can be made out of the categories
defined in the Blog *and*, additionally, out of the ones defined by the BlogFolder(s) it sits in. All the 
categories will add up. This feature can be useful when the Blog is 
maintained by several authors. You can then incorporate some policy that certain Entries must be
created in specific BlogFolders because of the additional categories. Categories you can later search for but you
don't want exposed to all the other authors.

Next to categories defined by the Blog object and the BlogFolders, you can also define a 
set of global categories. These categories are available to all the BlogEntries created in the portal. 
Defining these global categories can be done in ZMI in the simpleblog_tool or in the Plone setup.

BlogEntries can be searched for in the Catalog and in Topics using categories. Use the EntryCategory index.

Portlets

    SimpleBlog comes with 3 different portlets. One portlet (/here/portlet_simpleblog/macros/portlet)
shows a calendar, recent additions and categories. Another portlet (/here/portlet_simpleblog/macros/portlet-recent)
only shows the recent items and the last one ((/here/portlet_simpleblog/macros/portlet-comments), shows the 
most recent comments in the blog. The first two portlets can also be used outside the context of a blog. 
In that situation it will gather all the entries from all the blogs in all the subfolders, starting from 
the location of where this portlet is viewed.

Configuring SimpleBlog

    SimpleBlog allows you to control a few things in its behavior. In ZMI you can alter a few properties in 
the simpleblog_tool or, when you use Plone 2.0, you can go to Plone setup and go to the SimpleBlog control
panel. The following properties can be set:

    * **publishedState**: the name of the workflow state that indicates when the BlogEntry is 
published. Usually this will be set to 'published' but if your state is called differently in your workflow, then 
you can change it here. This state is used when SimpleBlog searches for 
BlogEntries that can be displayed on the front-page. So, if no Entries show up, 
check the workflow state of the BlogEntry and check if this property is correct. And check if the BlogEntries
themselves have the proper state and make sure the user has the proper permissions to view the entries even
when they are in the published state. (If entries still don't show up and you're sure you've checked everything, 
contact me).

    * **maxItemsInPortlet**: Tells how many BlogEntries are shown inside the portlets when SimpleBlog 
displays the most recent BlogEntries.

    * **globalCategories**: Lists the categories that are globally available in all BlogEntries in the portal.
    
    * **createPortletOnBlogCreation **: By default, when you create a new Blog, SimpleBlog will create the portletBlogFull_local
portlet. You can turn this feature off by un-checking this option.

**Note**: In the SimpleBlog control panel inside Plone setup, these variables are called a bit differently but the explanations
will be sufficient.

Well, that's all you have to know to set up SimpleBlog. Enjoy it.

Danny Bloemendaal (danny.bloemendaal@companion.nl)

PS: I'd like to thank everybody in #plone and everybody who sent me their suggestions for 
modifications and additions.