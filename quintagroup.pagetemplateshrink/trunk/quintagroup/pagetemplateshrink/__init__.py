from zope.tal.htmltalparser import HTMLTALParser
from zope.tal.talgenerator import TALGenerator
from zope.pagetemplate import pagetemplate

import re
expression = re.compile('[ \n\f\r]+(?=</?(?:me)?tal)')
expression2 = re.compile('\n\s*\n+(?= *<)')

def cook(self):
    """Compile the TAL and METAL statments.

    Cooking must not fail due to compilation errors in templates.
    """
    engine = self.pt_getEngine()
    source_file = self.pt_source_file()
    if self.content_type == 'text/html':
        gen = TALGenerator(engine, xml=0, source_file=source_file)
        parser = HTMLTALParser(gen)
    else:
        gen = TALGenerator(engine, source_file=source_file)
        parser = TALParser(gen)

    self._v_errors = ()
    try:
        #### the patch
        text = self._text
        text = expression.sub('', text)
        text = expression2.sub('', text)
        parser.parseString(text)
        #parser.parseString(self._text)
        self._v_program, self._v_macros = parser.getCode()
    except:
        self._v_errors = ["Compilation failed",
                          "%s: %s" % sys.exc_info()[:2]]
    self._v_warnings = parser.getWarnings()
    self._v_cooked = 1

pagetemplate.PageTemplate._old_cook = pagetemplate.PageTemplate._cook
pagetemplate.PageTemplate._cook = cook