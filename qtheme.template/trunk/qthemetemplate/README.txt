======================
qplone3 theme template
======================

Plan
-------------------------
1. Overview
2. Creating theme package
3. Extending theme
4. Release theme package


==========================
Overview
==========================

This theme template allow you to create plone3 theme python package 
with nested namespace. Initial package is theme package skeleton.
Than this package could be extended (fill in) with:
 - skin-layer(s),
 - portlet(s),
 - viewlet(s),
 - css, js resource(s).

Creation package performed with *paster create* PasteScript command.
Extending theme with other resources doing with *paster addcontent*
local ZopeSkel command (extended in this product).


==========================
Creating theme package
==========================

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
    >>> ls(package_dir)
    MANIFEST.in
    ...
    plone.example-configure.zcml
    ...
    quintagroup
    ...
    setup.py


*qplone3_theme* template - creates theme with nested namespace.

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
    


Theme holds 3 subdirectory (browser, profiles, skins)::
    >>> cd('quintagroup/theme')
    >>> dirs = ('skins', 'browser', 'profiles')
    >>> [True for d in dirs if d in os.listdir('ploneexample')]
    [True, True, True]

And initialization files (__init__.py, configure.zcml) ::
    >>> files = ('__init__.py', 'configure.zcml')
    >>> [True for d in files if d in os.listdir('ploneexample')]
    [True, True]
    

*browser* directory
------------------------

Browser directory contains:
  - 'templates' resource directory
  - interfaces.py module with IThemeSpecific marker interface.
  - configure.zcml, with registered theme marker interface.


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

As we see by default name of the theme is 'Custom Theme', but on theme
creation you can point own name. Check this ...

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


*skins* directory
------------------------

It's contain only README.txt file and NO SKIN LAYERS YET.
This job for localcommand ;)

But check am I right ...
    >>> cd('quintagroup/theme/ploneexample')
    >>> ls('skins')
    README.txt


*profiles* directory.
--------------------------------
There is 'default' and uninstall profiles in it
    >>> 'default' in os.listdir('profiles')
    True
    >>> 'uninstall' in os.listdir('profiles')
    True

In default profile there is:
 - import_steps.xml - for any reason.
 - skins.xml - register skins directory

    >>> cd('profiles/default')
    >>> 'import_steps.xml' in os.listdir('.')
    True
    >>> 'skins.xml' in os.listdir('.')
    True

*skins.xml* profile make your theme default on installation
and use layers list from 'Plone Default' for our theme,
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

Look to setuphandlers.py module
    >>> cd('../..')
    >>> cat('setuphandlers.py')
        def setupVarious(context):
    ...



=========================
Extending theme
=========================

One of the best features, which bring us ZopeSkel package - is *localcommand*.

In this part I show how you can extend a theme (generated with qplone3_theme
ZopeSkel template) with additional usefull staff:
  - skin layers
  - views
  - viewlets
  - portlets
  - css
  - javascripts

So in qplone3_theme generated package you can use *addcontent* ZopeSkel
local command.

IMPORTANT TO NOTE, that localcommand (addcontent in our case) should be
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


We see list of extention subtemplates, which can be used for our theme.
'N' character tell us that this subtemplates are registered for other (archetype)
template, but no metter - it can correctly extend our theme.


Adding SKIN LAYER
==========================

Use *skin_layer* subtemplate for that with *addcontent* local command

    >>> paster('addcontent --no-interactive skin_layer')
    paster addcontent --no-interactive skin_layer
    Recursing into profiles
    ...

This command add NEW 'skin_layer' (default name) directory to _skins_ directory,
with only CONTENT.txt file inside.

    >>> 'skin_layer' in os.listdir('skins')
    True
    >>> ls('skins/skin_layer')
    CONTENT.txt

*skins.xml* profile also updated:

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



Adding PORTLET
==========================

In portlets directory before adding new portlet present only
initialization files.

    >>> ls('portlets')
    __init__.py
    configure.zcml

Add portlet with *portlet* subtemplate.

    >>> paster('addcontent --no-interactive portlet')
    paster addcontent --no-interactive portlet
    Recursing into portlets
    ...

After executing this local command ...

In configure.zcml of the theme root directory - includes portlets registry:

    >>> cat('configure.zcml')
    <configure
    ...
    <include package=".portlets" />
    ...

In portlets directory added exampleportlet.pt template and exampleportlet.py script 
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

Finally new portlet type registered in portlets.xml profile

    >>> cat('profiles/default/portlets.xml')
    <?xml version="1.0"?>
    ...
       <portlet
         addview="quintagroup.theme.ploneexample.portlets.ExamplePortlet"
         title="Example portlet"
         description=""
       />
    ...

Thank ZopeSkel developers for this subtempalte ;)



Adding CSS resource
==============================

Use *css_resource* subtemplate.

    >>> paster("addcontent --no-interactive css_resource")
    paster addcontent --no-interactive css_resource
    Recursing into browser
    ...
    Recursing into profiles
    ...

This template add (if not yet exist) _stylesheets_ directory in _browser_
directory

    >>> 'stylesheets' in os.listdir('browser')
    True

In _stylesheets_ resource directory added empty main.css stylesheet
resource

    >>> 'main.css' in os.listdir('browser/stylesheets')
    True
    >>> cat('browser/stylesheets/main.css')
    <BLANKLINE>


New resource directory registered in configure.zcml

    >>> cat('browser/configure.zcml')
    <configure
    ...
        <browser:resourceDirectory
            name="quintagroup.theme.ploneexample.stylesheets"
            directory="stylesheets"
            layer=".interfaces.IThemeSpecific"
            />
    ...
    

And in profiles/default directory added cssregistry.xml profile with
registered main.css stylesheet

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



Adding JAVASCRIPT resource
------------------------------

Use *js_resource* subtemplate.

    >>> paster('addcontent --no-interactive js_resource')
    paster addcontent --no-interactive js_resource
    Recursing into browser
    ...
    Recursing into profiles
    ...

This template add (if not yet exist) _scripts_ directory in _browser_
directory

    >>> 'scripts' in os.listdir('browser')
    True


Empty foo.js javascript file added to _scripts_ directory

    >>> 'foo.js' in os.listdir('browser/scripts')
    True
    >>> cat('browser/scripts/foo.js')
    <BLANKLINE>


New resource directory registered in configure.zcml, if not yet registered.

    >>> cat('browser/configure.zcml')
    <configure
    ...
        <browser:resourceDirectory
            name="quintagroup.theme.ploneexample.scripts"
            directory="scripts"
            layer=".interfaces.IThemeSpecific"
            />
    ...
    

In profiles/default directory added (if not yet exist) cssregistry.xml profile,
and register new foo.js javascript resource.

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
For that case you can use *viewlet_order* subtemplate

    >>> paster('addcontent --no-interactive viewlet_order')
    paster addcontent --no-interactive viewlet_order
    Recursing into browser
    ...
    Recursing into templates
    ...
    Recursing into profiles
    ...

This template adds (if not exist ;)) _viewlets.py_ module in browser directory.

    >>> 'viewlets.py' in os.listdir('browser')
    True
    
    >>> cat('browser/viewlets.py')
    from Products.CMFCore.utils import getToolByName
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    from plone.app.layout.viewlets import common
    ...
    class Example(common.PersonalBarViewlet):
        render = ViewPageTemplateFile('templates/example_viewlet.pt')
    <BLANKLINE>

In viewlets.py module added viewlet class with example_viewlet.pt template.

Check template file in templates directory.

    >>> 'example_viewlet.pt' in os.listdir('browser/templates')
    True
    >>> cat('browser/templates/example_viewlet.pt')
    <BLANKLINE>

New viewlet registered in configure.zcml

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
    

In profiles/default directory added viewlets.xml profile with registration
with registration new viewlet, ordered for specified viewlet manager.

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



Hide EXISTANT viewlet
------------------------------

For that case you can use *viewlet_hidden* subtemplate

    >>> paster('addcontent --no-interactive viewlet_hidden')
    paster addcontent --no-interactive viewlet_hidden
    Recursing into profiles
    ...

As we see from upper log - there is adding/updating only profiles staff.
    

Look into profiles/default directory

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


Adding importing ZEXPs
------------------------------
This subtemplate allow you to add to your theme ZEXP objects, which will be exporting
into portal root on theme installation

    >>> paster('addcontent --no-interactive import_zexps')
    paster addcontent --no-interactive import_zexps
    ...
    Recursing into import
    ...
    Recursing into profiles
    ...
    Inserting from setuphandlers.py_insert into ...
    ...

As we see from upper log - there is:
   - adding 'import' directory into theme directory;
   - update profiles staff.
   - insert some staff into setuphandlers.py module
    
1. Look into 'import' directory:
    >>> ls('import')
    CONTENT.txt

It's empty - here you can put any zexp objects for install into portal root.


2. Look into profiles/default directory

    >>> ls('profiles/default')
    cssregistry.xml
    import_steps.xml
    ...


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

We see, that in import_steps.xml, added 'Import zexp' step.

3. Check setuphandlers.py module - there is must be importZEXPs function defined

    >>> cat('setuphandlers.py')
    def setupVarious(context):
    ...
    def importZEXPs(context):
    ...

So everything fine with setuphandlers too ;)


