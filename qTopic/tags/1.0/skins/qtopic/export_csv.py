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
    context.REQUEST.RESPONSE.setHeader('Content-Disposition', 'attachment; filename="%s.csv"'% context.getId())

res = context.queryCatalog()
fields = fields or context.getCustomViewFields()
csv_data = []
for r in res:
    csv_data.append(dict([(f, getattr(r, f, ''))for f in fields]))
return context.toCSV(fields, csv_data)
