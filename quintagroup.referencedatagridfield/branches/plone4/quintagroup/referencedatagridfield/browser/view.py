from archetypes.referencebrowserwidget.browser.view import \
         ReferenceBrowserPopup

class ReferenceDataGridBrowserPopup(ReferenceBrowserPopup):
    """ Extend default ReferenceBrowserPopup view with  properties,
        needed for ReferenceDataGridBrowserPopup
    """

    def __init__(self, context, request):
        super(ReferenceDataGridBrowserPopup, self).__init__(context, request)

        self.fieldTitleName = request.get('fieldTitleName','')
        self.fieldLinkName = request.get('fieldLinkName','')
        self.order_idx = request.get('order_idx', -1)

