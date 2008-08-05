======================
qplone3 theme template
======================

This theme allow you to create plone3 theme python package 
with nested namespace.

For create such theme use `paster create` command::

    >>> paster('create -t qplone3_theme plone.example --no-interactive')
    paster create -t qplone3_theme plone.example --no-interactive
    ...

Let's check the content of created plone.example package::

    >>> package_dir = 'plone.example'
    >>> ls(package_dir)
    MANIFEST.in
    README.txt
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
    __init__.pyc
    theme

    >>> cd('quintagroup')
    >>> ls('theme')
    __init__.py
    __init__.pyc
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
