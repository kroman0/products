qPloneResolveUID

Plone ResolveUID (qPloneResolveUID) product allows to replace existing
resolve uids with real urls usable for visitors and search engines.

Resolve uids is a very powerful tool to prevent broken links in Plone based sites.
kupu when used in conjunction with Archetypes generates urls that look like:
<a href="resolveuid?uid=a89073b893240c899008d0988903f89980" />
When inside Zope, resolveuid is actually a script that will resolve
the UID to a URL and direct the user there.

qPloneResolveUID product allows to generate real links instead of ulgy UIDs.
This product makes links more usable to visitors and search engines while content
manager see links with UIDs.

qPloneResolveUID product uses portal_transforms tool.
This product adds new transformation to transformation line during page generation process.


INSTALATION

   install qPloneResolveUID with quickinstaller in Plone


AUTHORS

   Melnychuk Taras, quintagroup.com.