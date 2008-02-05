Plone4ArtistsAudioPatch

    Plone4ArtistsAudioPatch is small proof of concept patch for 
    Plone4ArtistsAudio package.

    The problem which is addressed in this product is text 
    encoding issues in mp3 audio tags.

    The case.

        If you edit your mp3 tags in your own language (non English)
        with Windows based mp3 tag editors (winamp for example). The
        result tags will be saved in Windows default encoding (for 
        Cyrrilic it will be cp1251). The specifications of id3 tags
        as of version 2.4 define only three options for encoding 
        'Default' (for Latin-1), 'UTF-8' and 'UTF-16'. This mean that 
        if you populate your mp3 audio track id3 tags in non Cyrrilic 
        windows or Linux or Web you in most cases will see some 
        garbled symbols.

    With the product we give the website author, who uploads his mp3 
    track, option to guess the real text encoding of the mp3 tags 
    and convert the strings into UTF.

    The product is not supposed to be used in production (will not be
    supported) it is published as proposal for Plone4ArtistsAudio 
    authors to include the feature in the Plone4ArtistsAudio codebase.

    The Plone4ArtistsAudioPatch was tested with 
    Plone4ArtistsAudio1.0-alpha1

AUTHORS

    Bogdan Koval mentored by Volodymyr Cherepanyak, Myroslav Opyr
