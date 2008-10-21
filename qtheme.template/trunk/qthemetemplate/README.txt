======================
qplone3 theme template
======================

Overview
-------------------------

This theme template allow you to create plone3 theme python package 
with nested namespace. Initial package is theme package skeleton.
Than this package could be extended with:
 - skin-layer(s),
 - portlet(s),
 - viewlet(s),
 - css, js resource(s).

Creation package performed with `paster create` PasteScript command.
Extending theme with other resources doing with `paster addcontent`
local ZopeSkel command (extended in this product).

Let's create theme package
---------------------------

For create such theme use `paster create` command::

    >>> paster('create -t qplone3_theme plone.example --no-interactive --overwrite')
    paster create -t qplone3_theme plone.example --no-interactive
    ...

Let's check the content of created plone.example package::

    >>> package_dir = 'plone.example'
    >>> ls(package_dir)
    MANIFEST.in
    README.txt
    ...
    plone.example-configure.zcml
    ...
    quintagroup
    ...

So you have python package with *quintagroup* upper level namespace.
Also there are *README.txt* with information about your theme, 
*plone.example-configure.zcml* - zcml file for adding into package-includes
directory 


With qplone3_theme template - creates theme with nested namespace.
By default - theme placed in 

    quintagroup.theme.<package name without dot> namespace

in our case - quintagroup.theme.ploneexample


So check namespaces::
    >>> 'quintagroup' in os.listdir(package_dir)
    True

    >>> cd(package_dir)
    >>> 'theme' in os.listdir('quintagroup')
    True

    >>> path = os.path.join('quintagroup','theme')
    >>> 'ploneexample' in os.listdir(path)
    True
    


Package holds 3 subdirectory (browser, profiles, skins) and 
initialization files::
    >>> cd('quintagroup/theme')
    >>> ls('ploneexample')
    __init__.py
    browser
    configure.zcml
    portlets
    profiles
    profiles.zcml
    setuphandlers.py
    skins
    skins.zcml
    tests.py
    version.txt


Review browser directory
------------------------

In browser directory created 'templates' resource directory
for views, viewlets, ...; interfaces.py module with IThemeSpecific
marker interface. In configure.zcml register theme marker interface.


    >>> cd('ploneexample')
    >>> ls('browser')
    __init__.py
    configure.zcml
    interfaces.py
    templates

    >>> cat('browser/interfaces.py')
    from plone.theme.interfaces import IDefaultPloneLayer
    <BLANKLINE>
    class IThemeSpecific(IDefaultPloneLayer):
    ...

    >>> cat('browser/configure.zcml')
    <configure
    ...
        <interface
            interface=".interfaces.IThemeSpecific"
            type="zope.publisher.interfaces.browser.IBrowserSkinType"
            name="Custom Theme"
            />
    ...

As we saw by default name of the theme is 'Custom Theme', but on theme
creation you can point own name. Check it ...

First create configuration file with other skin name
    >>> conf_data = """
    ... [pastescript]
    ... skinname=My Theme Name
    ... """
    >>> file('theme_config.conf','w').write(conf_data)

Create same theme with own skin name and check this
    >>> paster('create -t qplone3_theme plone.example --no-interactive --overwrite --config=theme_config.conf')
    paster create ...
    >>> cd(package_dir)
    >>> cat('quintagroup/theme/ploneexample/browser/configure.zcml')
    <configure
    ...
        <interface
            interface=".interfaces.IThemeSpecific"
            type="zope.publisher.interfaces.browser.IBrowserSkinType"
            name="My Theme Name"
            />
    ...


Now lets vew to skins directory of generated theme - it's contain only
README.txt file and no skin layers yet. This job for localcommand ;)
But check am I right ...
    >>> cd('quintagroup/theme/ploneexample')
    >>> ls('skins')
    README.txt


Now check profiles directory.
--------------------------------
There is 'default' profile in it
    >>> ls('profiles')
    default

In default profile there is:
 - import_steps.xml - for any reason.
 - skins.xml - register skins directory

    >>> cd('profiles/default')
    >>> ls('.')
    import_steps.xml
    ...
    skins.xml

Skins profile make your theme default on installation
and base layers list on 'Plone Default' theme, without
any new layers.
    >>> cat('skins.xml')
    <?xml version="1.0"?>
    <object name="portal_skins" ...
            default_skin="My Theme Name">
    ...
    <skin-path name="My Theme Name" based-on="Plone Default">
      <!-- -*- extra layer stuff goes here -*- -->
    <BLANKLINE>
    </skin-path>
    ...

import_steps.xml - connect setupVarious function from
setuphandlers module for additional installation steps.
    >>> cat('import_steps.xml')
    <?xml version="1.0"?>
    ...
    <import-step id="quintagroup.theme.ploneexample.various"
    ...
                 handler="quintagroup.theme.ploneexample.setuphandlers.setupVarious"
    ...
    </import-step>
    ...

View for setuphandlers.py module
    >>> cd('../..')
    >>> cat('setuphandlers.py')
        def setupVarious(context):
    ...



=========================
Test localcommnands
=========================

One of the best features, which bring us ZopeSkel package - is localcommand.

Now review localcommands = possibility to extend your theme with additional
staff - skin layers, views, viewlets, portlets, css and javascript resources


qplone3_theme generated package theme support ZopeSkel local command 'addcontent'.

    >>> paster('addcontent -a')
    paster addcontent -a
      ...
        css_resource:    A Plone 3 CSS resource template
      ...
        js_resource:     A Plone 3 JS resource template
      N portlet:         A Plone 3 portlet
      ...
        skin_layer:      A Plone 3 Skin Layer
      ...
      N view:            A browser view skeleton
        viewlet_hidden:  A Plone 3 Hidden Viewlet template
        viewlet_order:   A Plone 3 Order Viewlet template
      ...


So you can extend your theme with following subtemplates:
  - portlet
  - skin layer
  - css resource
  - js resource
  - viewlet (order/hidden)
  - view
'N' character tell us that this subtemplates are registered for other (archetype)
template, but no metter - it can correctly extend our theme.

Skin layer
------------
Review what changes when adding skin_layer to the theme

    >>> paster('addcontent --no-interactive skin_layer')
    paster addcontent --no-interactive skin_layer
    Recursing into profiles
    ...

Now check skins directory - new 'skin_layer' (default name) directory must be added,
which contain only CONTENT.txt file
    >>> 'skin_layer' in os.listdir('skins')
    True
    >>> ls('skins/skin_layer')
    CONTENT.txt

There is also skins.xml profile must be updated:
    >>> cat('profiles/default/skins.xml')
    <?xml version="1.0"?>
    <object name="portal_skins" allow_any="False" cookie_persistence="False"
       default_skin="My Theme Name">
    ...
     <object name="skin_layer"
        meta_type="Filesystem Directory View"
        directory="quintagroup.theme.ploneexample:skins/skin_layer"/>
    <BLANKLINE>
     <skin-path name="My Theme Name" based-on="Plone Default">
    ...
      <layer name="skin_layer"
         insert-after="custom"/>
    <BLANKLINE>
     </skin-path>
    ...

We see, that: 
  - skin_layer directory registered as Filesystem Directory View
  - skin_layer Filesystem Directory View added to our theme layers list





Test of portlet adding
------------------------------

Review portlets directory before adding new portlet

    >>> ls('portlets')
    __init__.py
    configure.zcml

Add portlet
    >>> paster('addcontent --no-interactive portlet')
    paster addcontent --no-interactive portlet
    Recursing into portlets
    ...

In configure.zcml included registries from portlets:
    >>> cat('configure.zcml')
    <configure
    ...
    <include package=".portlets" />
    ...

Check changes in portlets directory
    >>> ls('portlets')
    __init__.py
    configure.zcml
    exampleportlet.pt
    exampleportlet.py

In portlets/configure.zcml - should register new portlet
    >>> cat('portlets/configure.zcml')
    <configure
    ...
         <plone:portlet
             name="quintagroup.theme.ploneexample.portlets.ExamplePortlet"
             interface=".exampleportlet.IExamplePortlet"
             assignment=".exampleportlet.Assignment"
             view_permission="zope2.View"
             edit_permission="cmf.ManagePortal"
             renderer=".exampleportlet.Renderer"
             addview=".exampleportlet.AddForm"
             editview=".exampleportlet.EditForm"
             />
    ...

And now review configure.zcml profile
    >>> cat('profiles/default/portlets.xml')
    <?xml version="1.0"?>
    ...
       <portlet
         addview="quintagroup.theme.ploneexample.portlets.ExamplePortlet"
         title="Example portlet"
         description=""
       />
    ...

So new portlet registered.



Test of css_resource
------------------------------

    >>> paster("addcontent --no-interactive css_resource")
    paster addcontent --no-interactive css_resource
    Recursing into browser
    ...
    Recursing into profiles
    ...

From upper log - we see that there is adding/updating some staff
in browser and profiles directories

    >>> ls('browser')
    __init__.py
    ...
    stylesheets
    ...

There is added styles resource directory with empty main.css stylesheet
resource

    >>> ls('browser/stylesheets')
    README.txt
    main.css
    >>> cat('browser/stylesheets/main.css')
    <BLANKLINE>

By default it is added empty main.css file


But this new resource directory also should be registered in configure.zcml

    >>> cat('browser/configure.zcml')
    <configure
    ...
        <browser:resourceDirectory
            name="quintagroup.theme.ploneexample.stylesheets"
            directory="stylesheets"
            layer=".interfaces.IThemeSpecific"
            />
    ...
    

Now look into profiles/default directory

    >>> ls('profiles/default')
    cssregistry.xml
    ...
    >>> cat('profiles/default/cssregistry.xml')
    <?xml version="1.0"?>
    <object name="portal_css">
    <BLANKLINE>
     <stylesheet title=""
        id="++resource++quintagroup.theme.ploneexample.stylesheets/main.css"
        media="screen" rel="stylesheet" rendering="inline"
        cacheable="True" compression="safe" cookable="True"
        enabled="1" expression=""/>
    ...

We see, that in cssregistry.xml, registries new main.css stylesheet resource.



Test of js_resource
------------------------------

    >>> paster('addcontent --no-interactive js_resource')
    paster addcontent --no-interactive js_resource
    Recursing into browser
    ...
    Recursing into profiles
    ...

From upper log - we see that there is adding/updating some staff
in browser and profiles directories

    >>> ls('browser')
    __init__.py
    ...
    scripts
    ...

There is added scripts resource directory with empty foo.js javascript

    >>> ls('browser/scripts')
    README.txt
    foo.js
    >>> cat('browser/scripts/foo.js')
    <BLANKLINE>

By default it is added empty foo.js file


But this new resource directory also should be registered in configure.zcml

    >>> cat('browser/configure.zcml')
    <configure
    ...
        <browser:resourceDirectory
            name="quintagroup.theme.ploneexample.scripts"
            directory="scripts"
            layer=".interfaces.IThemeSpecific"
            />
    ...
    

Now look into profiles/default directory

    >>> ls('profiles/default')
    cssregistry.xml
    ...
    jsregistry.xml
    ...
    >>> cat('profiles/default/jsregistry.xml')
    <?xml version="1.0"?>
    <object name="portal_javascripts">
    ...
     <javascript
        id="++resource++quintagroup.theme.ploneexample.scripts/foo.js"
        inline="False" cacheable="True" compression="safe"
        cookable="True" enabled="1"
        expression=""
        />
    ...

We see, that in jsregistry.xml, registries new foo.js javascript resource.


Test viewlets subtemplates:
==============================

There is 2 types of viewlet subtemplate:
 - viewlet_order
 - viewlet_hidden

Of the two subtemplates, the former is for adding new viewlet and
set order for it in ViewletManager, other one only hide viewlet in
pointed ViewletManager


Ordered NEW viewlet
------------------------------
For that case you can use viewlet_order subtemplate

    >>> paster('addcontent --no-interactive viewlet_order')
    paster addcontent --no-interactive viewlet_order
    Recursing into browser
    ...
    Recursing into templates
    ...
    Recursing into profiles
    ...

From upper log - we see that there is adding/updating some staff
in browser and profiles directories

    >>> ls('browser')
    __init__.py
    ...
    viewlets.py

Added viewlets.py python module

    >>> cat('browser/viewlets.py')
    from Products.CMFCore.utils import getToolByName
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    from plone.app.layout.viewlets import common
    ...
    class Example(common.PersonalBarViewlet):
        render = ViewPageTemplateFile('templates/example_viewlet.pt')
    <BLANKLINE>

We see that added viewlet class with example_viewlet.pt template.
Check if exist this template in templates directory

    >>> ls('browser/templates')
    README.txt
    example_viewlet.pt

There is also empty example_viewlet.pt template.

    >>> cat('browser/templates/example_viewlet.pt')
    <BLANKLINE>

This new viewlet must be registered in configure.zcml

    >>> cat('browser/configure.zcml')
    <configure
    ...
       <browser:viewlet
            name="quintagroup.theme.ploneexample.example"
            manager="plone.app.layout.viewlets.interfaces.IPortalHeader"
            class=".viewlets.Example"
            permission="zope2.View"
            />
    ...
    

Now look into profiles/default directory

    >>> ls('profiles/default')
    cssregistry.xml
    ...
    viewlets.xml

    >>> cat('profiles/default/viewlets.xml')
    <?xml version="1.0"?>
    <object>
    ...
     <order manager="plone.portalheader"
             based-on="Plone Default"
             skinname="My Theme Name" >
    ...
        <viewlet name="quintagroup.theme.ploneexample.example" insert-after="*" />
    <BLANKLINE>
      </order>
    <BLANKLINE>
    </object>

We see, that in viewlets.xml, ordered new viewlet for plone.portalheader viewlet manager.


Hide EXISTANT viewlet
------------------------------
For that case you can use viewlet_hidden subtemplate

    >>> paster('addcontent --no-interactive viewlet_hidden')
    paster addcontent --no-interactive viewlet_hidden
    Recursing into profiles
    ...

As we see from upper log - there is adding/updating only profiles staff.
    

So look into profiles/default directory

    >>> ls('profiles/default')
    cssregistry.xml
    ...
    viewlets.xml

    >>> cat('profiles/default/viewlets.xml')
    <?xml version="1.0"?>
    <object>
    ...
      <hidden manager="plone.portalheader" skinname="My Theme Name">
    ...
        <viewlet name="example" />
    <BLANKLINE>
      </hidden>
    ...
    </object>

We see, that in viewlets.xml, hide example viewlet for plone.portalheader viewlet manager.


