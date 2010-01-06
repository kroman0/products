browserlayer archetype sub-template
===================================

The browserlayer sub-template allows you to extend package, created with
archetype zopeskel template.

So, first create archetype base package:

    >>> paster('create -t archetype plone.example --no-interactive --overwrite')
    paster create -t archetype plone.example --no-interactive
    ...

Go into the package and check presence of *interfaces* and *profiles* directories

    >>> cd('plone.example','plone','ploneexample')
    >>> ls('.')
    README.txt
    ...
    interfaces
    ...
    profiles
    ...

Now verify if interface/__init__.py contains IPloneExample browser layer interface,
and there is no profiles/default/browserlayer.xml section in default generic setup
profile.

     >>> cat('interfaces/__init__.py')
     # -*- extra stuff goes here -*-
     <BLANKLINE>


Check that there is no browserlayer.xml present in the default profile

    >>> cat('profiles', 'default', 'browserlayer.xml')
    No file named profiles/default/browserlayer.xml

Add browser layer ...

    >>> paster('addcontent browserlayer')
    paster ...
    Inserting ... into .../plone.example/plone/ploneexample/interfaces/__init__.py
    ...
    Copying ... to .../plone.example/plone/ploneexample/profiles/default/browserlayer.xml

Now  IPlonePloneexample interface must be added to interfaces/__init__.py module

     >>> cat('interfaces/__init__.py')
     # -*- extra stuff goes here -*-
     ...
     class IPlonePloneexample(Interface):
     ...

And browserlayer.xml step must present in default generic setup profile:

    >>> cat('profiles', 'default', 'browserlayer.xml')
    <?xml version="1.0"?>
    <layers>
       <layer name="plone.ploneexample"
         interface="plone.ploneexample.interfaces.IPlonePloneexample"/>
    </layers>
    <BLANKLINE>

