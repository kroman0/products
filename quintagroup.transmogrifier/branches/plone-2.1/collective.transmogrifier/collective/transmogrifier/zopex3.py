try:
    from zope.component import provideUtility, provideAdapter, adapts
except ImportError:
    from zope.app import zapi
    from zope.app.servicenames import Adapters

    def provideAdapter(factory, adapts=None, provides=None, name=''):
        method=getattr(zapi.getGlobalService(Adapters), 'register')
        method(adapts, provides, name, factory)

    def provideUtility(component, provides=None, name=u''):
        method=getattr(zapi.getGlobalService('Utilities'), 'provideUtility')
        if provides is None:
            provides = list(component.__providedBy__)[0]
        method(provides, component, name)

    def adapts(*args, **kwargs):
        pass

    import zope.component
    zope.component.provideAdapter = provideAdapter
    zope.component.provideUtility = provideUtility
    zope.component.adapts = adapts
