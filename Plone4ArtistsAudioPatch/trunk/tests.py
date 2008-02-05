from unittest import TestSuite

def test_suite():
    suite = TestSuite()
    
    name = 'p4a.audiopatch.tests.test_docintegrationtests'
    m = __import__(name, (), (), name)
    try:
        suite.addTest(m.test_suite())
    except AttributeError, e:
        raise AttributeError(m.__name__+': '+str(e))
                
    return suite
