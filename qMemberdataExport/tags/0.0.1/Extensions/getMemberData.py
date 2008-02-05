def getMemberData(context):

    import csv
    from cStringIO import StringIO
    from DateTime import DateTime
    from Products.CMFCore.utils import getToolByName

    mdtool = getToolByName(context, 'portal_memberdata')
    mtool = getToolByName(context, 'portal_membership')

    props = ['id',] + mdtool.propertyIds()
    members = mtool.listMembers()

    res = StringIO()
    writer = csv.DictWriter(res, fieldnames = props, quoting=csv.QUOTE_ALL)

    # writing header row
    writer.writer.writerow(props)

    for member in members:
        properties = {}
        for propid in props:
            properties[propid] = member.getProperty(propid, '')
        writer.writerow(properties)

    context.REQUEST.RESPONSE.setHeader('Content-Type', 'text/csv')
    context.REQUEST.RESPONSE.setHeader('Content-Disposition', 'attachment; filename= memberdata-%s.csv' % DateTime().strftime("%Y-%m-%d-%H-%M-%S"))

    return res.getvalue()