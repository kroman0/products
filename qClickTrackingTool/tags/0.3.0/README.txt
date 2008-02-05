Quintagroup Click Tracking Tool

  The product is aimed for assisting in tracking advertisement campaigns in 
  Plone websites. It cooperates with AWstats statistical analysis engine
  that does heavilifting. Toll simplifies Plone management of campains
  for decision makers. Simplifying task for developers linking to campaigns.

  "Product Homepage":http://quintagroup.com/services/plone-development/products/click-tracking-tool |
  "Download":http://sourceforge.net/projects/quintagroup

  (c) "Quintagroup":http://quintagroup.com/ , 2005. 

  support@quintagroup.com * quintessence of modern business

Usage

  1. Install with Quick Installer. 

  2. Go to Plone Setup -> Click Tracking Tool

  3. Create your Campaigns (Links) there. Important are id (campaign Id) and 
     URL (the address tool should direct campaign to).

  4. Add following section to your awstats.*config*.conf::

       ExtraSectionName1="Tracked clicks"
       ExtraSectionCodeFilter1="200 302 304"
       ExtraSectionCondition1="URL,^\/track\/.*"
       ExtraSectionFirstColumnTitle1="Transition"
       ExtraSectionFirstColumnValues1="URL,^/track\/([^/]+)(\/)?"
       ExtraSectionStatTypes1=H
       MaxNbOfExtra1=50
       MinHitExtra1=1

     If you have ExtraSection 1 in your config, change 1 to next 
     available number.

  5. Add banners/tabs, links on the site to point your campaigns in the 
     Tracking tool: "/track/campaignId".

  6. Watch your awstats, it should have "Tracked clicks" section with collected
     data grouped per campaign.
     
Authors

  * Myroslav Opyr

  * Taras Melnychuk
