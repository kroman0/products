def getMemberData(self, start=0, batch=400, exclude_props=None, include_props=None):

    import csv
    from cStringIO import StringIO
    from DateTime import DateTime
    from Products.qMemberdataExport import getRegisteredMemberdataHandlers as registry
    from Products.qMemberdataExport.config import EXCLUDE_PROPS, CLEAR_CACHE_COUNTER

    if exclude_props is None: exclude_props = EXCLUDE_PROPS

    memberdatahandler = False

    for handler in registry():
        try:
            memberdatahandler = handler(self)
            break
        except:
            pass

    if not memberdatahandler: return None

    members = memberdatahandler.getAllMembers()

    if batch > len(members) - start: batch = len(members) - start

    members_list = []
    counter = 0

    for member in members[start:start+batch]:
        counter += 1
        if counter % CLEAR_CACHE_COUNTER == 0: 
            self._p_jar.sync()
        members_list.append(memberdatahandler.getMemberProperties(member, exclude_props, include_props))

    res = StringIO()
    writer = csv.DictWriter(res, fieldnames = memberdatahandler.fieldnames, quoting=csv.QUOTE_ALL)

    # writing header row
    writer.writer.writerow(memberdatahandler.fieldnames)
    # writing body of csv file
    writer.writerows(members_list)

    # setting headers for attaching file
    self.REQUEST.RESPONSE.setHeader('Content-Type', 'text/csv')
    self.REQUEST.RESPONSE.setHeader('Content-Disposition', 'attachment; filename=memberdata-%s.csv' % DateTime().strftime("%Y-%m-%d-%H-%M-%S"))

    return res.getvalue()
