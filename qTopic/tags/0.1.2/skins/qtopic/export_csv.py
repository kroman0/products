## Script (Python) "isATCTbased"
##title=Formats the history diff
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=download=0,fields=None,show_header=1
if download:
    context.REQUEST.RESPONSE.setHeader('Content-Type', 'plain/text')
    context.REQUEST.RESPONSE.setHeader('Content-Disposition', 'attachment; filename="%s.csv"' % context.getId())
res = context.queryCatalog()
fields = fields or context.getExportFields()
delimiter = context.getDelimiter() or ';'
if show_header and context.getShowHeader():
   print delimiter.join(fields)
for r in res:
   print delimiter.join([test(getattr(r, f, ''),getattr(r, f, ''),'') for f in fields])
return printed