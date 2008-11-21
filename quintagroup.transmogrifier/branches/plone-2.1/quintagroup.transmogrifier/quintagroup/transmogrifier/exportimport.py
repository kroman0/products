from zope.interface import implements

from collective.transmogrifier.interfaces import ITransmogrifier
from collective.transmogrifier.transmogrifier import _load_config, constructPipeline

try:
    from Products.GenericSetup import context as gscontext
except ImportError:
    from Products.CMFSetup import context as gscontext

from quintagroup.transmogrifier.writer import WriterSection
from quintagroup.transmogrifier.reader import ReaderSection

EXPORT_CONFIG = 'export'
IMPORT_CONFIG = 'import'

def exportSiteStructure(context):
    transmogrifier = ITransmogrifier(context.getSite())

    # we don't use transmogrifer's __call__ method, because we need to do
    # some modification in pipeline sections

    transmogrifier._raw = _load_config(EXPORT_CONFIG)
    transmogrifier._data = {}

    options = transmogrifier._raw['transmogrifier']
    sections = options['pipeline'].splitlines()
    pipeline = constructPipeline(transmogrifier, sections)

    last_section = pipeline.gi_frame.f_locals['self']

    # if 'quintagroup.transmogrifier.writer' section's export context is
    # tarball replace it with given function argument
    while hasattr(last_section, 'previous'):
        if isinstance(last_section, WriterSection) and \
            isinstance(last_section.export_context, gscontext.TarballExportContext):
            last_section.export_context = context
        last_section = last_section.previous
        # end cycle if we get empty starter section
        if type(last_section) == type(iter(())):
            break
        last_section = last_section.gi_frame.f_locals['self']

    # Pipeline execution
    for item in pipeline:
        pass # discard once processed

def importSiteStructure(context):
    # this function is also called when adding Plone site, so call standard handler
    if not context.readDataFile('.objects.xml', subdir='structure'):
        try:
            from Products.GenericSetup.interfaces import IFilesystemImporter
            IFilesystemImporter(context.getSite()).import_(context, 'structure', True)
        except ImportError:
            pass
        return

    transmogrifier = ITransmogrifier(context.getSite())

    # we don't use transmogrifer's __call__ method, because we need to do
    # some modification in pipeline sections

    transmogrifier._raw = _load_config(IMPORT_CONFIG)
    transmogrifier._data = {}

    options = transmogrifier._raw['transmogrifier']
    sections = options['pipeline'].splitlines()
    pipeline = constructPipeline(transmogrifier, sections)

    last_section = pipeline.gi_frame.f_locals['self']

    # if 'quintagroup.transmogrifier.writer' section's export context is
    # tarball replace it with given function argument
    while hasattr(last_section, 'previous'):
        if isinstance(last_section, ReaderSection) and \
            isinstance(last_section.import_context, gscontext.TarballImportContext):
            last_section.import_context = context
        last_section = last_section.previous
        # end cycle if we get empty starter section
        if type(last_section) == type(iter(())):
            break
        last_section = last_section.gi_frame.f_locals['self']

    # Pipeline execution
    for item in pipeline:
        pass # discard once processed
