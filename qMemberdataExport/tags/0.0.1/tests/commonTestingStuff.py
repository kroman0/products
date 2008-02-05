from DateTime import DateTime

from Products.CMFCore.utils import getToolByName

from Products.PloneTestCase import PloneTestCase

from Products.qMemberdataExport.config import *

PRODUCTS=('qMemberdataExport',)

map(PloneTestCase.installProduct, PRODUCTS)
PloneTestCase.setupPloneSite(products=PRODUCTS)

PRODUCT = 'qMemberdataExport'

def maps_login(self, role):
    """  Utility method for login under required role """
    from Testing.ZopeTestCase.PortalTestCase import user_name, user_password
    if role == 'manager':
        self.loginAsPortalOwner()
    elif role == 'member':
        self.login(user_name)
    elif role == 'another_member':
        self.login('another_member')
    elif role == 'anonym':
        self.logout()

def parseCSV(self, data):
    """ Utility function for parsing csv and extracting some data form portal_memberdata """
    import csv
    from cStringIO import StringIO

    props = ['id',] + getToolByName(self.portal, 'portal_memberdata').propertyIds()
    reader = csv.DictReader(StringIO(data), fieldnames = props, quoting=csv.QUOTE_ALL)
    i = 0
    res = []
    for row in reader:
        properties = {}
        if i != 0 and row['id'] != 'test_user_1_':
            for field in row.keys():
                if field in PROPERTIES_TO_COMPARE: properties[field] = row[field]
            res.append(properties)
        i += 1
    self.failUnless(i-2 == len(PORTAL_MEMBERS), 'CSV output does not matcht to amount of portal members')
    members = [memb.copy() for memb in PORTAL_MEMBERS]
    for memb in members: del memb['roles']
    return (members, res)

def addMember(self, username, fullname, email, roles, last_login_time):
    """ Utility function for simpler way of adding portal members with default password 'secret' """
    self.membership.addMember(username, 'secret', roles, [])
    member = self.membership.getMemberById(username)
    member.setMemberProperties({'fullname': fullname, 'email': email,
                                'last_login_time': DateTime(last_login_time),})

# testing stuff for adding members to portal

PROPERTIES_TO_COMPARE = ['id', 'fullname', 'email', 'last_login_time']

PORTAL_MEMBERS = [{
                   'id'              : 'Fred',
                   'fullname'        : 'Fred Flintstone',
                   'email'           : 'fred@bedrock.com',
                   'roles'           : ['Member', 'Reviewer'],
                   'last_login_time' : '2002/01/01'},
                  {
                   'id'              : 'admin',
                   'fullname'        : 'Admin',
                   'email'           : 'admin@admin.com',
                   'roles'           : ['Manager'],
                   'last_login_time' : '2003/12/28'},
                  {
                   'id'              : 'barney',
                   'fullname'        : 'Barney Rubble',
                   'email'           : 'barney@bedrock.com',
                   'roles'           : ['Member'],
                   'last_login_time' : '2002/01/01'},
                  {
                   'id'              : 'brubble',
                   'fullname'        : 'Bambam Rubble',
                   'email'           : 'bambam@bambam.net',
                   'roles'           : ['Member'],
                   'last_login_time' :  '2003/12/31'},
                 ]
