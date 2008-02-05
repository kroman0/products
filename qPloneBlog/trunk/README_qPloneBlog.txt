qPloneBlog

qPloneBlog is a SimpleBlog based product with refactorings and extendings.


APPLIED FEATURES:

  - categorization
  - technorati tags support
  - trackback supporting with management and spam defense
  - pinging
  - RSS1, RSS2 syndication
  - allow working with Blogger, Weblog, MetaWeblog APIs
  - bookmarklets
  - Google adsence management in blog pages


PACKAGE's PRODUCTS:

  * SimpleBlog v.qg2.5
  * qPingTool v.0.3
    * qRSS2Syndication v. 0.5
    * XMLRPCMethod, v.XMLRPC Method-1-1
  * RPCAuth v.0.1.0-final
  * qTrackSpam (extender product) v.0.2
  * adsenseproduct (extender product) v.0.1


DEPENDENCIES:

  * Plone v.2.1+
  * Archetypes v.1.3.5 and above
  * ATContentTypes v.1.0.1-final and above


INSTALLATION

  * downloads qPloneBlog package
  * put all package's products to Plone's Product directory
  * in ZMI create RPCAuth object in the rooty of your Plone instance.
  * using quickinstaller install SimpleBlog, qPingTool, qRSS2Syndication,
    qTrackSpam and adsenseproduct


PRODUCT SETUP AND TUNING

  * SimpleBlog:
    * in plone control panel go to SimpleBlog setup.
      Here is portal wide options for blogs.

  * Pinging:
    * in ZMI in portal_pingtool input web address of your site
    * in ZMI in portal_syndication:
        * allow syndication in portal_pingtool/propertiesForm
        * allow syndication tab visibility in 
          portal_syndication/manage_editActionsForm
    * in plone control panel go to Ping Tool setup.
      Here you can add, delete, change ping info for pinging sites list.
    * go to Blog or BlogFolder, which you wish to ping.
      * in syndication tab - allow syndication
      * in added 'ping setup' tab - enable pinging and select desired ping
        sites and save this settings.
        * here you can ping container's content to selected sites
          whenever you want.

  * Trackback management:
    You have 2 configlets in plone control panel:
      * BlackList Importer
        Allow you form URL's black list - both: by direct Black list
        editing or by file uploading.
        black list records interprets as regular expressions.
      * Clean TrackBacks
        Allow manage new (not published) trackbacks: mark as black and 
        remove, publish.
        Represent all trackbacks from all portal's blogs in table.

  * Adsense in blogs
    Allow adding google adsense block in Blog entries.
      * go to plone control panel to Adsense Properties and input
        you customer Id

  * Blog API
    For working with blog and it's content through external application,


DESCRIPTION:

  qPloneBlog is an easy to use Plone based weblog application with fore 
portal types: Blog, BlogFolder, BlogEntry and  Trackback:
  Blog - Folderish object that is the container for the BlogEntries and the
         front-page of the weblog.
  BlogEntry - Entry object inside the weblog.
  BlogFolder - Folder that can only exist inside the Blog container.
               The folder allows you to organize the BlogEntries in any way
               you like.
  Trackback - trackback to other blog-post (web resource possible).
              Can be added only to BlogEntry type object.
              Contains short information about blog-post, which links to blog
              entry, where trackback URL, of this BlogEntry is added.
              Can be in two workflow states: pending and published.


GETTING STARTED

  You can go to any folder that you have permissions for and add
a Blog from any of the dropdown lists. You will be given a form
where you can provide the necessary information to create a new Blog:

  * **Short Name**, **Title**, **Description** will speak for themselves.

  * **Maximum number of blog entries to display** defines how many
    items should be visible on the Blog's front-page.

  * **Available entry Categories**, **Tags** is a list of categories
    and tags accordingly, that can be used inside BlogEntries
    (one category or tag per line).

After clicking on **next** button you will go to next blog's
**[interface]** property list and provide appropriate customizations:

  * **Show warning for unpublished entries** - turning on/off displaying 
    warning on the blog's frontpage if there are entries that are not 
    yet published.

  * **Show Byline footer**, **Show Icons** - checkboxes for switching on/off
    appearance accordingly footer and icon for BlogEntry. 

  * **Enable technorati tags** and **Allow Trackback** - will speak
    for themselves.

  * **Turn ... bookmarklet** - turn on/off appearance appropriate
    bookmarklet in the Byline footer.

  * **Turn top Adsence block** and **Turn bottom Adsence block** -
    turn on/off top and bottom google adsense blocks for blog entries.

  * **Select top adsence template** and **Select bottom adsence template** -
    give you possibility to chose an adsense template.

After you have created the Blog, you can adjust its Display settings from the
Display menu in Plone. Currently there are 3 different display settings.
Besides these settings, there is also a stylesheet in product's skin that you
can customize at will.

After you have created the Blog, you can start creating BlogEntries.
Choose BlogEntry from the Add items list and fill in the form:

  * **Short Name**, **Title**, **Teaser**, **Body** will speak for
      themselves. **Note** when you use the Upload a file field, be aware
      that it will replace the current content!!

  * **Always on top** Controls if the Entry, when published is always shown
    first. This can be handy for announcements etc.

  * **Categories** Select one or more categories from the list to classify
    the BlogEntry.

  * **Tags** - allow you select or add tag(s) for technorati.com

  * **sendTrackBackURLs** - a list of trackback URLs (one per line). On
    publishing this blog entry, information about it sends to URLs.

  * **Digg topic** - Choose the digg topic for symplify blog entry readers
    digging this entry.

  * **Related items** point to other content in your portal to indicate them
    as related.

  * **Allow Discussion on this item** control whether people can comment on
    this entry.

After the BlogEntry is saved, it will be in the 'draft' workflow state and is
only visible by the owner and the manager (by default). So, in order to make
it appear on the Blog's front-page, it must be set in the 'published' state
The Blog will search and display the BlogEntries that have this state (this
state is defined in the simpleblog_tool in ZMI and in the configlet in Plone
setup). When putting the BlogEntry in the published state, you can also choose
to give it an effective date somewhere in the future. SimpleBlog uses the
standard way of publishing content.

Inside the Blog you can create BlogFolders. These are a bit similar to the
Blog itself in that it has roughly the same view but this time it only shows
the Entries that are stored inside the BlogFolder (and subfolders).
BlogFolders are there for your convenience, to organize or archive Entries in
any way you want and to have additional categories (see below).

To BlogEntry also Trackback can be added. Trackback include following fields:

  * **Short Name**, **Title**, **Description** will speak for themselves.

  * **Url**, **Blog_name** and **excerpt** point to URL, Blog's name and
    excerpt accordingly of trackbacked blog post, frow witch this blog entry
    was linked in.

Commonly trackbacks added by blog itself (trackback system). After adding
Trackback presents in **pending** state and on defoult permissions set is
visible only for Manager and Owner roles. After publishing - it's visible
for all.


CATEGORIES

  qPloneBlog can use categories to classify BlogEntries. When you edit and
configure the Blog object, you can provide it with a list of categories that
will present itself as a multi-selection list when you edit/create a BlogEntry.
Next to that, BlogFolders can define additional categories.
In BlogEntries created inside the BlogFolder, a selection can be made out of
the categories defined in the Blog *and*, additionally, out of the ones
defined by the BlogFolder(s) it sits in. All the categories will add up. This
feature can be useful when the Blog is maintained by several authors. You can
then incorporate some policy that certain Entries must be created in specific
BlogFolders because of the additional categories. Categories you can later
search for but you don't want exposed to all the other authors.

  Next to categories defined by the Blog object and the BlogFolders, you can
also define a set of global categories. These categories are available to all
the BlogEntries created in the portal. Defining these global categories can
be done in ZMI in the simpleblog_tool or in the Plone setup.

  BlogEntries can be searched for in the Catalog and in Topics using 
categories. Use the EntryCategory index.


TECHNORATI TAGS

  qPloneBlog support Technorati tags if following manner: in **Tags** field
of BlogEntry - you may point existent or add new tag(s). On the BlogEntry
view page - you may view pointed tags. Clicking one of the BlogEntry =tag=
bring you to page "Everything tagged =tag=", on www.technorati.com.


TRACKBACKS

  qPLoneBlog support trackback system.
  BlogEntry can be both trackback source (BE-source) and trackback holder
(BE-holder).
  BE-source provide **trackback URL** and register short information about
every BE-holder in Trackback-type objects, by adding Trackbacks to
BE-source.
  BE-holder add **trackback URL** of BE-sources (to field 
**sendTrackBackURLs**). On publishing BE-holder short information about it
sends to list of **trackback URL**s.

**trackback URL** - present on BlogEntry view page.
**Trackback** object automatically creates and added in BE-source on
publishing BE-holder.
New created Trackback object appear in pending workflow state. Manager or
Owner can publish or delete Trackback object.
Trackbacks is visible only in navigation tree.

It is qTrackSpam product, which provide trackback management
(http://projects.quintagroup.com/products/wiki/qTrackSpam)
For manage trackbacks it is 2 configlets in plone control panel:
**BlackList importer** and **Clean TrackBacks**.
  * **BlackList importer** - allow manage with blac list filters. Every line
      in BlackList presents separate filter. Actually filter is regular
      expression, which apply to **Url** field of new added trackback.
  * **Clean TrackBacks** - is form to site wide trackbacks managements, which
      allow you to select group of trackback(s) and publish or blacklist and
      remove selection.


PINGING

(http://projects.quintagroup.com/products/wiki/qPingTool)
  qPloneBlog allows ping Blog or BlogFolder to one or more ping servers.
For pinging working - syndication should be allowed for portal in
portal_syndiction/propertiesForm, and also should be allowed syndication for
pingin container (Blog/BlogFolder), which can be done by go to syndication tab
on pingin container (Blog/BlogFolder) or if it invisible - go to
[pinging container URL]/synPropertiesForm URL. After that on pingin container
adds **ping setup** tab, wich allow you to tune pinging and perform pinging of
course. After perform pingign, information about pinging results appear in
"portal message" block.
  For add, delete pinging site(s) or change its properties - you should go to
plone control panel to **Ping setup** and operate with Ping Info objects. This
type object has following properties:
    * Title ping site's name
    * URL - ping site's URL
    * Method_name - name of RPC method (get from ping site instructions)
    * RSS_version - set version of RSS, which used to form result page for
      ping site. Default - "Blog", leave default value if you don't now
      exactly what you are doing.



OTHER FEATURES

  * RSS2 SUPPORT with qRSS2Syndication product
    (http://projects.quintagroup.com/products/wiki/qRRS2Syndication)

  * BLOGGER APIS
    qPloneBlog provide 3 blogger APIs:
      - MetaWeblog API
      - MovableType API
      - Blogger API
    You need not to perform any tuning in Blog or portal - only in Blogger
    apllication for use this possibility.

  * BOOKMARKLETS
    As was mentioned earlier, on Blog editing page, on interface shemata
    settings you will see 5 checkboxes **Turn ... bookmarklet**, which manage
    bookmarklets appearance on BlogEntry footer.

  * GOOGLE ADSENSE
      On Blog editing page, on interface shemata also presernt 2 checkboxes:
    **Turn ... Adsence block** with self explanatory labels. It is important
    to notise, that this checkboxes switches google adsense appearance in
    **every BlogEntry of the blog**.
      Other tuning google adsense block possibility is selection block type
    for each top and bottom blocks. This featchure also present on interface
    schemata
    of Blog edit page.
      And at last - you have to go to plone control panel, to
    **Adsense Properties** and enter **customer Id**, got from Google.

