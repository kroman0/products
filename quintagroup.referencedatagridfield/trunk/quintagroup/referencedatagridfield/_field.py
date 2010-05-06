#from Products.Archetypes import atapi
import re
import logging
import urlparse
from urllib import quote
from types import ListType, TupleType

from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.validation import validation #validators import baseValidators
from Products.Archetypes.Field import encode
from Products.Archetypes.Registry import registerField, registerWidget

from Products.DataGridField.DataGridField import DataGridField
from Products.DataGridField.DataGridWidget import DataGridWidget


# Logger object
#logger = logging.getLogger('ReferenceDataGridField')
#logger.debug("ReferenceDataGrid loading")

class ReferenceDataGridWidget(DataGridWidget):
    _properties = DataGridWidget._properties.copy()
    _properties.update({
        'macro' : "referencedatagridwidget",
        })

isURL = validation.validatorFor('isURL')

class ReferenceDataGridField(DataGridField):
    _properties = DataGridField._properties.copy()
    _properties.update({
        'columns' : ('title', 'link_uid'),
        'widget': ReferenceDataGridWidget,
        })

    security = ClassSecurityInfo()

    security.declarePrivate('isRemoteURL')
    def isRemoteURL(self, url):
        if isURL(url) == 1:
            return True
        return False

    security.declarePrivate('set')
    def set(self, instance, value, **kwargs):
        """
        The passed in object should be a records object, or a sequence of dictionaries
        About link_uid data:
          * interpretations:
            * if data not starts with standard protocol names (http://, ftp://) it treats
              as UID
          * record removed if:
            * no data;
            * data contains UID of not existent object
        About title:
          * if there is UID of existent object and record has not title data
            - object's Title will be used.
        """
        catalog = getToolByName(instance, "uid_catalog")

        if value is None:
            value = ()

        if not isinstance(value, (ListType, TupleType)):
            value = value,

        result = []
        for row in value:
            data = {"title":"", "link_uid":""}

            title = str(row.get('title', "")).strip()
            if not title == "":
                data["title"] = title

            url = str(row.get('link_uid', "")).strip()
            if url == '':
                continue
            elif self.isRemoteURL(url):
                data["link_uid"] = urlparse.urlunparse(urlparse.urlparse(url))
            else:
                brains = catalog(UID=url)
                if len(brains) == 0:
                    continue
                else:
                    data["link_uid"] = url
                    if title == "":
                        data["title"] = getattr(brains[0], "Title","")
            result.append(data)

        DataGridField.set(self, instance, result, **kwargs)

    security.declarePrivate('get')
    def get(self, instance, **kwargs):
        """ Return DataGridField value

        Value is a list object of rows.
        Row id dictionary object with standard 'link_uid' and 'title' keys
        plus extra informal *isLink* key
        """
        purl = getToolByName(instance, "portal_url")
        resuid = purl() + "/resolveuid/"

        result = []
        rows = DataGridField.get(self, instance, **kwargs)
        for row in rows:
            data = {"link_uid": row["link_uid"],
                    "title": row["title"],
                    "link": ""}
            url = row["link_uid"]
            if self.isRemoteURL(url):
                data["link"] = quote(url, safe='?$#@/:=+;$,&%')
            else:
                data["link"] = resuid + url
            result.append(data)

        return result

registerWidget(
    ReferenceDataGridWidget,
    title='DataGrid Reference',
    used_for=('quintagroup.referencedatagridfield.ReferenceDataGridField',)
    )

registerField(
    ReferenceDataGridField,
    title="DataGrid Reference Field",
    description=("Reference DataGrid field.")
    )
