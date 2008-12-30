from interfaces import IDomainsMapExtractor

def add_domains_map(context, event):
    """Add to request PATH-DOMAIN map.
    """
    pd_map = None
    extractor = IDomainsMapExtractor(context, None)
    if extractor is not None:
        pd_map = extractor.getDomainsMap()

    if pd_map is not None:
        event.request.set('path_domain_map', pd_map)

