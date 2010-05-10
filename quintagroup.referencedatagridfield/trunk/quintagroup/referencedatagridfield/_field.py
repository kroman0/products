#from Products.Archetypes import atapi
import re
import logging
import urlparse
from urllib import quote
from types import ListType, TupleType

from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.validation import validation #validators import baseValidators
from Products.Archetypes.Field import encode, ReferenceField
from Products.Archetypes.Registry import registerField, registerWidget

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

from Products.DataGridField.DataGridField import DataGridField
from Products.DataGridField.DataGridWidget import DataGridWidget


# Logger object
#logger = logging.getLogger('ReferenceDataGridField')
#logger.debug("ReferenceDataGrid loading")

class ReferenceDataGridWidget(DataGridWidget, ReferenceBrowserWidget):
    _properties = ReferenceBrowserWidget._properties.copy()
    _properties.update(DataGridWidget._properties.copy())
    _properties.update({
        'macro': "referencedatagridwidget",
        'column_names': ['Title', 'Link or UID'],
        'helper_css': ('datagridwidget.css',),
        'helper_js': ('referencebrowser.js', 'datagridwidget.js',),
        'force_close_on_insert': True,
        })

isURL = validation.validatorFor('isURL')

class ReferenceDataGridField(DataGridField, ReferenceField):
    _properties = ReferenceField._properties.copy()
    _properties.update(DataGridField._properties.copy())
    _properties.update({
        'columns': ('title', 'link_uid'),
        'widget': ReferenceDataGridWidget,
        'multiValued' : True,
        })

    security = ClassSecurityInfo()

    security.declarePrivate('isRemoteURL')
    def isRemoteURL(self, url):
        return isURL(url) == 1 and True or False

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

        uids = []
        result = []
        for row in value:
            data = {"title":"", "link_uid":""}

            title = str(row.get('title', "")).strip()
            if not title == "":
                data["title"] = title

            link_uid = str(row.get('link_uid', "")).strip()
            if link_uid == '':
                continue
            elif self.isRemoteURL(link_uid):
                data["link_uid"] = urlparse.urlunparse(urlparse.urlparse(link_uid))
            else:
                brains = catalog(UID=link_uid)
                if len(brains) == 0:
                    continue
                # Found objects with pointed UID
                uids.append(link_uid)
                brain = brains[0]
                data["link_uid"] = link_uid
            result.append(data)

        DataGridField.set(self, instance, result, **kwargs)
        ReferenceField.set(self, instance, uids, **kwargs)
        
    security.declarePrivate('get')
    def get(self, instance, **kwargs):
        """ Return DataGridField value

        Value is a list object of rows.
        Row id dictionary object with standard 'link_uid' and 'title' keys
        plus extra informal *isLink* key
        """
        purl = getToolByName(instance, "portal_url")
        catalog = getToolByName(instance, "portal_catalog")

        result = []
        uids = {}
        rows = DataGridField.get(self, instance, **kwargs)
        for row in rows:
            result.append({"link_uid": row["link_uid"],
               "title": row["title"],
               "link": ""})
            data = result[-1]
            # Process remote URL and collect UIDs
            link_uid = row["link_uid"]
            if self.isRemoteURL(link_uid):
                data["link"] = quote(link_uid, safe='?$#@/:=+;$,&%')
                # if title not set for remote url - set it equals to url
                if not data["title"]:
                    data["title"] = link_uid
            else:
                uids[link_uid] = data
            
        # Process UIDs
        if uids:
            brains = catalog(UID=uids.keys())
            for b in brains:
                data = uids[b.UID]
                data["link"] = b.getURL()
                # If title not set - get it from the brain
                if not data["title"]:
                    data["title"] = self._brains_title_or_id(b, instance)

        return result

    def getRaw(self, instance, **kwargs):
        """Return raw data DataGridField data."""
        return DataGridField.getRaw(self, instance, **kwargs)


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
