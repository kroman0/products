======================
qplone3 theme template
======================

This theme template allow you to create plone3 theme python package 
with nested namespace.

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


Test of portlet adding
    >>> paster('addcontent --no-interactive portlet')
    paster addcontent --no-interactive portlet
    Recursing into portlets
    ...



Test of css_resource
    >>> paster("addcontent --no-interactive css_resource")
    paster addcontent --no-interactive css_resource
    Recursing into browser
    ...
    Recursing into profiles
    ...

Test of js_resource
    >>> paster('addcontent --no-interactive js_resource')
    paster addcontent --no-interactive js_resource
    Recursing into browser
    ...
    Recursing into profiles
    ...



Exceptions for last two templates raised because of both templates
expect for path to file object with data with appropriate content
for that resource.
