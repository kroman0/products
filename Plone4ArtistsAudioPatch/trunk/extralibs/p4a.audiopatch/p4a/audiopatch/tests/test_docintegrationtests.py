def test_suite():
    from unittest import TestSuite

    suite = TestSuite()

    if has_plone():
        import os
        from App import Common
        from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite
        from p4a.audiopatch.tests.ploneintegration import testclass_builder
        from Products.PloneTestCase import layer

        pkg_home = Common.package_home({'__name__': 'p4a.audiopatch.tests'})
        samplesdir = os.path.join(pkg_home, 'samples')


	from p4a.audio.mp3.thirdparty import eyeD3
		
	samplefile = os.path.join(samplesdir, 'test-cyrrilic.mp3')
	mimetype = 'audio/mpeg'	
	encoding = 'WINDOWS-1251'
	
	t = eyeD3.Tag()
	t.link(samplefile)
	
	eyeD3_encoding = 'latin_1'

        fields = dict(
            title=t.getTitle().encode(eyeD3_encoding).decode(encoding),
            artist=t.getArtist().encode(eyeD3_encoding).decode(encoding),
            album=t.getAlbum().encode(eyeD3_encoding).decode(encoding),
            )

	suite.addTest(ZopeDocFileSuite('plone-audio-impl.txt', package='p4a.audiopatch',
		test_class=testclass_builder(samplefile=samplefile,
					required_mimetype=mimetype,
					file_content_type='File',
					fields=fields,
					tag_encoding=encoding,
					eyeD3_encoding=eyeD3_encoding)
	)
	)


        suite.layer = layer.ZCMLLayer

    return suite

def has_plone():
    try:
        import Products.CMFPlone
    except ImportError, e:
        return False
    return True
