qplone3 theme template
======================

Contents
--------
1. Overview
2. Creating theme package
3. Extending theme
4. Release notes

Overview
========

This theme template allows you to create plone3 theme python package 
with nested namespace. Initial package is theme package skeleton.
This package can be extended (filled in) with:

  - skin-layer(s)
  - portlet(s)
  - viewlet(s)
  - css, js resource(s)

Creation of a package is performed with *paster create* PasteScript command.
Theme extending with other resources can be done with *paster addcontent*
local ZopeSkel command (extended in this product).

Creating theme package
======================

Let's create plone-3 theme python package.
Use `paster create` command for that::

    >>> paster('create -t qplone3_theme plone.example --no-interactive --overwrite')
    paster create -t qplone3_theme plone.example --no-interactive
    ...

You got standard python package content with 
  - *quintagroup* upper level namespace.
  - *plone.example-configure.zcml* - zcml file 
    for adding into package-includes directory

Check that::

    >>> package_dir = 'plone.example'
    >>> objects = ('setup.py', 'quintagroup', 'plone.example-configure.zcml')
    >>> [True for o in objects if o in os.listdir(package_dir)]
    [True, True, True]


*qplone3_theme* template - creates theme with nested namespace.

By default - theme is placed in

    quintagroup.theme.<package name without dot> namespace

in our case - quintagroup.theme.ploneexample

So check namespaces::
    >>> theme_namespace = os.path.join(package_dir,'quintagroup','theme','ploneexample')
    >>> os.path.isdir(theme_namespace)
    True

Theme holds 3 subdirectories (browser, profiles, skins)::
    >>> cd(theme_namespace)
    >>> dirs = ('skins', 'browser', 'profiles')
    >>> [True for d in dirs if d in os.listdir('.')]
    [True, True, True]

And initialization files (__init__.py, configure.zcml) ::
    >>> files = ('__init__.py', 'configure.zcml')
    >>> [True for d in files if d in os.listdir('.')]
    [True, True]
    

*browser* directory
-------------------

Browser directory contains:
  - 'templates' resource directory
  - interfaces.py module with IThemeSpecific marker interface
  - configure.zcml, with registered theme marker interface

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

As we see, default theme name is 'Custom Theme', but on theme
creation you can point out your own name. Check this ...

First create configuration file with different skin name
    >>> conf_data = """
    ... [pastescript]
    ... skinname=My Theme Name
    ... """
    >>> file('theme_config.conf','w').write(conf_data)

Create the same theme with your own skin name and check this
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


*skins* directory
------------------------

It contains only README.txt file and NO SKIN LAYERS YET.
This is a job for localcommand ;)

But check whether I am right ...
    >>> cd('quintagroup/theme/ploneexample')
    >>> ls('skins')
    README.txt


*profiles* directory.
--------------------------------
There is 'default' and uninstall profiles inside
    >>> 'default' in os.listdir('profiles')
    True
    >>> 'uninstall' in os.listdir('profiles')
    True

There are the following items in default profile:
 - import_steps.xml - for any reason.
 - skins.xml - for registering skins directory

    >>> cd('profiles/default')
    >>> 'import_steps.xml' in os.listdir('.')
    True
    >>> 'skins.xml' in os.listdir('.')
    True

*skins.xml* profile makes your theme default on installation
and uses layers list from 'Plone Default' for our theme,
without any new layers (yet).

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

*import_steps.xml* - call _setupVarious_ function from
_setuphandlers.py_ module for additional installation steps.

    >>> cat('import_steps.xml')
    <?xml version="1.0"?>
    ...
    <import-step id="quintagroup.theme.ploneexample.various"
    ...
                 handler="quintagroup.theme.ploneexample.setuphandlers.setupVarious"
    ...
    </import-step>
    ...

Look at setuphandlers.py module
    >>> cd('../..')
    >>> cat('setuphandlers.py')
        def setupVarious(context):
    ...


Extending theme
===============

One of the best features, which ZopeSkel package brings, is *localcommand*.

In this part I will show how you can extend a theme (generated with qplone3_theme
ZopeSkel template) with additional useful stuff:

  - skin layers
  - views
  - viewlets
  - portlets
  - css
  - javascripts

So, in qplone3_theme generated package you can use *addcontent* ZopeSkel
local command.

IMPORTANT TO NOTE: localcommand (addcontent in our case) should be
called in any subdirectory of the generated theme package. And it won't
work outside this package..

    >>> paster('addcontent -a')
    paster addcontent -a
      ...
        css_resource:    A Plone 3 CSS resource template
      ...
        import_zexps:    A template for importing zexp-objects into portal on installation
        js_resource:     A Plone 3 JS resource template
      N portlet:         A Plone 3 portlet
      ...
        skin_layer:      A Plone 3 Skin Layer
      ...
      N view:            A browser view skeleton
        viewlet_hidden:  A Plone 3 Hidden Viewlet template
        viewlet_order:   A Plone 3 Order Viewlet template
      ...


We can see a list of extention subtemplates, which can be used for our theme.
'N' character tells us that these subtemplates are registered for other (archetype)
template, but it does not matter - they can correctly extend our theme.


Adding SKIN LAYER
=================

For that case use *skin_layer* subtemplate with *addcontent* local command

    >>> paster('addcontent --no-interactive skin_layer')
    paster addcontent --no-interactive skin_layer
    Recursing into profiles
    ...

This command adds NEW 'skin_layer' (default name) directory to _skins_ directory,
with only CONTENT.txt file inside.

    >>> 'skin_layer' in os.listdir('skins')
    True
    >>> ls('skins/skin_layer')
    CONTENT.txt

*skins.xml* profile is also updated:

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

We can see, that: 
  - skin_layer directory was registered as Filesystem Directory View
  - skin_layer Filesystem Directory View was added to our theme layers list


Adding PORTLET
==========================

Only initialization files are available in portlets directory before adding new portlet.

    >>> ls('portlets')
    __init__.py
    configure.zcml

Add portlet with *portlet* subtemplate.

    >>> paster('addcontent --no-interactive portlet')
    paster addcontent --no-interactive portlet
    Recursing into portlets
    ...

After executing this local command ...

configure.zcml file in the theme root directory - includes portlets registry:

    >>> cat('configure.zcml')
    <configure
    ...
    <include package=".portlets" />
    ...

exampleportlet.pt template and exampleportlet.py script added to portlets directory.
    >>> files = ('exampleportlet.pt', 'exampleportlet.py')
    >>> [True for d in files if d in os.listdir('portlets')]
    [True, True]

And portlets/configure.zcml - register new portlet
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

Finally, new portlet type is registered in portlets.xml profile

    >>> cat('profiles/default/portlets.xml')
    <?xml version="1.0"?>
    ...
       <portlet
         addview="quintagroup.theme.ploneexample.portlets.ExamplePortlet"
         title="Example portlet"
         description=""
       />
    ...

Thanks to ZopeSkel developers for this subtempalte ;)



Adding CSS resource
===================

Use *css_resource* subtemplate.

    >>> paster("addcontent --no-interactive css_resource")
    paster addcontent --no-interactive css_resource
    Recursing into browser
    ...
    Recursing into profiles
    ...

This template adds (if does not exist yet) _stylesheets_ directory in _browser_
directory

    >>> 'stylesheets' in os.listdir('browser')
    True

In _stylesheets_ resource directory empty main.css stylesheet
resource added

    >>> 'main.css' in os.listdir('browser/stylesheets')
    True
    >>> cat('browser/stylesheets/main.css')
    <BLANKLINE>


New resource directory was registered in configure.zcml

    >>> cat('browser/configure.zcml')
    <configure
    ...
        <browser:resourceDirectory
            name="quintagroup.theme.ploneexample.stylesheets"
            directory="stylesheets"
            layer=".interfaces.IThemeSpecific"
            />
    ...
    

And cssregistry.xml profile was added into profiles/default directory with
registered main.css stylesheet

    >>> 'cssregistry.xml' in os.listdir('profiles/default')
    True
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



Adding JAVASCRIPT resource
--------------------------

Use *js_resource* subtemplate.

    >>> paster('addcontent --no-interactive js_resource')
    paster addcontent --no-interactive js_resource
    Recursing into browser
    ...
    Recursing into profiles
    ...

This template adds (if does not exist yet) _scripts_ directory in _browser_
directory

    >>> 'scripts' in os.listdir('browser')
    True


Empty foo.js javascript file was added to _scripts_ directory

    >>> 'foo.js' in os.listdir('browser/scripts')
    True
    >>> cat('browser/scripts/foo.js')
    <BLANKLINE>


New resource directory was registered in configure.zcml, if has not been registered yet.

    >>> cat('browser/configure.zcml')
    <configure
    ...
        <browser:resourceDirectory
            name="quintagroup.theme.ploneexample.scripts"
            directory="scripts"
            layer=".interfaces.IThemeSpecific"
            />
    ...
    

cssregistry.xml profile was added into profiles/default directory (if does not exist yet),
and register new foo.js javascript resource.

    >>> 'jsregistry.xml' in os.listdir('profiles/default')
    True
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



Test viewlets subtemplates
==========================

There are 2 types of viewlet subtemplates:
 - viewlet_order
 - viewlet_hidden

The first one is used for adding new viewlets and setting 
viewlets order for the ViewletManager, the second one only hides
viewlet in pointed ViewletManager.

Ordered NEW viewlet
-------------------

Use *viewlet_order* subtemplate

    >>> paster('addcontent --no-interactive viewlet_order')
    paster addcontent --no-interactive viewlet_order
    Recursing into browser
    ...
    Recursing into templates
    ...
    Recursing into profiles
    ...

This template adds (if not exist ;)) _viewlets.py_ module in browser directory.
With added Example ViewletBase class, which is bound to templates/example_viewlet.pt
template

    >>> 'viewlets.py' in os.listdir('browser')
    True
    
    >>> cat('browser/viewlets.py')
    from Products.CMFCore.utils import getToolByName
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    from plone.app.layout.viewlets import common
    ...
    class Example(common.ViewletBase):
        render = ViewPageTemplateFile('templates/example_viewlet.pt')
    <BLANKLINE>

Check template file in templates directory.

    >>> 'example_viewlet.pt' in os.listdir('browser/templates')
    True
    >>> cat('browser/templates/example_viewlet.pt')
    <BLANKLINE>

New viewlet is registered in configure.zcml

    >>> cat('browser/configure.zcml')
    <configure
    ...
       <browser:viewlet
            name="quintagroup.theme.ploneexample.example"
            manager="plone.app.layout.viewlets.interfaces.IPortalHeader"
            class=".viewlets.Example"
            layer=".interfaces.IThemeSpecific"
            permission="zope2.View"
            />
    ...
    

viewlets.xml profile is added to profiles/default directory with new viewlet 
registration, ordered for specified viewlet manager.

    >>> 'viewlets.xml' in os.listdir('profiles/default')
    True
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



Hide EXISTING viewlet
---------------------

For that case you can use *viewlet_hidden* subtemplate

    >>> paster('addcontent --no-interactive viewlet_hidden')
    paster addcontent --no-interactive viewlet_hidden
    Recursing into profiles
    ...

As we see from upper log - there is stuff for adding/updating profiles only.
    

There is viewlet.xml profile in profiles/default directory
which hides viewlet for specified viewlet manager

    >>> 'viewlets.xml' in os.listdir('profiles/default')
    True
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


Adding ZEXPs importing
======================

Imagine situation, when you develop a theme, which uses some 
extra portal objects (documents with text for some potlets)
Then customer of your theme can edit these objects according
to his need.

For this situation *import_zexps* subtemplate exists.

*import_zexps* subtemplate extends your theme with
mechanism for importing list of zexp formated files
into portal root on theme instllation.

    >>> paster('addcontent --no-interactive import_zexps')
    paster addcontent --no-interactive import_zexps
    ...
    Recursing into import
    ...
    Recursing into profiles
    ...
    Inserting from setuphandlers.py_insert into ...
    ...

As we see from the upper log:
   - 'import' directory was added into root of the theme
   - profiles stuff was updated
   - some stuff into setuphandlers.py module was inserted
    
1. There was empty 'import' directory added, where you
   will put zexp objects for install into portal root.

    >>> ls('import')
    CONTENT.txt


2. import_steps.xml was added in profiles/default directory (if does not exist yet),
   which contains additional *quintagroup.theme.ploneexample.import_zexps* step.

    >>> 'import_steps.xml' in os.listdir('profiles/default')
    True

    >>> cat('profiles/default/import_steps.xml')
    <?xml version="1.0"?>
    <import-steps>
    ...
      <import-step id="quintagroup.theme.ploneexample.import_zexps"
                   version="..."
                   handler="quintagroup.theme.ploneexample.setuphandlers.importZEXPs"
                   title="My Theme Name: Import zexps objects">
        <dependency step="skins" />
        Import zexp objects into portal on My Theme Name theme installation
      </import-step>
    <BLANKLINE>
    </import-steps>

3. Check setuphandlers.py module - there must be importZEXPs function defined

    >>> cat('setuphandlers.py')
    def setupVarious(context):
    ...
    def importZEXPs(context):
    ...

Then simply prepare zexp objects and copy them to *import* directory.


RELEASE NOTES !
===============

Before releasing theme - I suggest to clean up setup.py script:

 - remove *theme_vars* argument (its value is useful only for
   theme development)

 - remove *entry_points* argument (same reason).
   It's useless in plone for now.

 - And remove *paster_plugins* argument too (it has sence
   in conjunction with entry_points during theme developing)

Steps mentioned above prevent possible problems with
theme distribution/deployment.
