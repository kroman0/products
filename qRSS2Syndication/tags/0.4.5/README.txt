qRSS2Syndication simple product that adds RSS2 functionality to Plone. 
   * includes support of audio and video feeds.
   * the syndication of ATAudio objects, mp3, wmv, ppt, jpg files using RSS 2.0 with enclosures.
   * full body of article <content:encoded> support for Documents and SimpleBlog.
   * Smart Folders/Topic syndication suported in Plone 2.1.2. The standart CMFTopic in Plone 2.0.5 does not implement getSyndicatableValues.
   * basic iTunes support


DEPENDS on:

   * CMFSyndication

INSTALATION:

1. install it with quickinstaller in Plone.


RSS2 syndiction properties are saved into the syndication_information object 
which is controled with portal_syndication tool

EXTENDING

If you need to introduce your custom content type into RSS2 refer to the document_item.pt template in the skin (or any other *_item.pt).

AUTHORS

Volodymyr Cherepanyak <chervol@quintagroup.com>
Wolfgang Reutz <wolfgang.reutz@fhv.at> - iTunes support, mediacoop audio/video support.  