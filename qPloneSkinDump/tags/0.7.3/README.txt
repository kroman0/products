Quintagroup Plone Skin Dump

  qPloneSkinDump allows to create Plone product
  (in file system) from some ZMI based skin folder
  (eg "custom") from portal_skins.

  So you can easy design new Plone skin with all
  customized styles, page tamplates, python scripts,
  ECMA-scripts, Images and other objects, located
  in some folder of portal_skins. Than dump it to
  new Plone Skin Product to file system.
  

Features:

  - Support dumping objects from generated portal's root
    to Skin Product for adding this objects to
    destination portal root on iinstalling Skin Product.

  - Dump css and ecma-cripts resources registries from 
    generated portal to Skin Product for right working
    styles and ecma-scripts.
    
  - Allow dumping sorce skin folder with subfolder tree.
    
  - Allow add aditional installation functions in config.py
    module generated Skin Product. 
    
  - Allow customize slots for generated Skin Product.
  
  - All configuration data for Skin Procut can be easy
    changed in file system, cause all constants has
    detailed explanations and examples.


Installation:

  1. Install qPloneSkinDump as Zope product

  2. Install qPloneSkinDump in your Plone instance with QuickInstaller
     (Plone Control Panel -> Add/remove Products)


Usage

  1. Create standart Plone Folder ( <folder-source> ) in portal_skins
     or use standard 'custom' folder and fill it with content according 
     to your needs. You can create subfolders in <folder-source>.

  2. Go to the Plone Control Panel, select "qPloneSkinDump Configuration"
     configlet and edit corresponding form fields:

     - <folder-source> is the name of the folder where all the content
        and styles are located in ZMI ../portal_skins/<folder-source>.

     - <ZMI Base Skin Name> is name of the Plone Skin, which list of layers
       will be used for creating new skin. (eg "Plone Tableless").

     - <Erace>  is checkbox for erasing <folder-source> folder
       from portal_skins after Product creating.

     - <Skin's Name>  is the name of skin folder for new product ( Actually
        Products/<Product name>/skin/<skin's name> ), that will be based
        on the <folder-source> staff.
        This <Skin's Name> also used as name of new Plone skin.

     - <Product name> - the name of new Plone product.

     - <Do customize slots> - Check it for PROVIDING SLOTS CUSTOMIZATION
        in New Skin Product.

     - <Left portal slots customizing>, <Right portal slots customizing>
        - left and right slots lists for New Plone Product. You are
        responsible for leaving only those portlets, which relate to your
        skin product or are standard for Plone.

     - <Slot's list forming> - slot's list forming control on New Plone
        Product installation.

     - <Main column> - decide in which column leave same slots, in case
        of meetings one.

     - <Exporting objects from portal root> - check it for export objects
       from your Portal root to Skin Product. Than chosed objects will be
       added to Portal root (where Skin Product will be installed) on
       installation.
     
     - <Import Policy> - define how will be imports objects to portal root
       on installation Skin Product if will be meeting same named (id)
       objects.
     
     - <Exporting objects> multyselected list for choosing objects from
       generated portal, which must be imported to portal root on Skin 
       Product's installation.
       
     - <Dump portal_CSS registry> - switch on|off dumping portal_css registry
       resources with all properties sets. Be attentive when switch-off this checkbox.
       When switch-on - all css-es of your new Skin Product and other portal_css
       resources will be sets identically to your settings and this guarantee
       identical look and behavior of your skeen on other Plone site.
     
     - <Dump portal_JS registry> - switch on|off dumping portal_javascripts registry
       resources with all properties sets. Be attentive when switch-off this checkbox.
       When switch-on - all ECMA-scripts of your new Skin Product and other 
       portal_javascripts resources will be sets identically to your settings 
       and this guarantee identical look and behavior of your skeen on other 
       Plone site.
     
  5. For using new Plone product you must reload Zope, and install it in quickinstaller.

  In file system new product located in ../Products/<Product name>.


Caution

    If you wish distribute generated Skin Product, you must
        - (for Plone 2.1+) before run generation remove all non-standard
          (for Plone dstribution) css and jvascripts resources from
          plone_css and plone_javascripts registries, which aren't 
          related to new Skin Product (not in the <folder-source>)
          

Authors

  * Andriy Mylenkyy


License

  * ZPL
