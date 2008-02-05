""" Utility functions """

def addCSS(container, sheetId, title, csshovering):
    """ Add DTML Method object to portal root """
    from OFS.DTMLMethod import addDTMLMethod
    addDTMLMethod(container, sheetId, title, csshovering)