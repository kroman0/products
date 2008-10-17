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
    distwriters.py
    docs
    plone.example-configure.zcml
    plone.example.egg-info
    quintagroup
    setup.cfg
    setup.py

So you have python package with *quintagroup* upper level namespace.

Now check namespaces::
    >>> cd(package_dir)
    >>> ls('quintagroup')
    __init__.py
    theme

    >>> cd('quintagroup')
    >>> ls('theme')
    __init__.py
    ploneexample

So we receave quitagroup.theme namespace with ploneexample python package.

Package holds 3 subdirectory (browser, profiles, skins) and 
initialization files::
    >>> cd('theme')
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

=========================
Test localcommnands
=========================
  This theme support ZopeSkel local command 'addcontent'.

    >>> paster('addcontent -a')
    paster addcontent -a
    ...

So you can extend your theme with following subtemplates:
  - portlet
  - skin layer
  - css resource
  - js resource
  - viewlet (order/hidden)

Check portlet
    >>> paster('addcontent -l')
    paster addcontent -l
    Available templates:
        css_resource:    A Plone 3 CSS resource template
        js_resource:     A Plone 3 JS resource template
        skin_layer:      A Plone 3 Skin Layer
        viewlet_hidden:  A Plone 3 Hidden Viewlet template
        viewlet_order:   A Plone 3 Order Viewlet template


Test of portlet adding
    >>> paster('addcontent --no-interactive portlet')
    paster addcontent --no-interactive portlet
    Recursing into portlets
    ...

Test of skin_layer adding
    >>> paster('addcontent --no-interactive skin_layer')
    paster addcontent --no-interactive skin_layer
    Recursing into profiles
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
