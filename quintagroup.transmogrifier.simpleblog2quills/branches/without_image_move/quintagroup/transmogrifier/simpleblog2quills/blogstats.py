#! /usr/bin/env python
import sys
import os.path
import fnmatch 
import re
from xml.dom import minidom
import time

def listFiles(root, patterns='*', recurse=1, return_folders=0): 
    # Expand patterns from semicolon-separated string to list 
    pattern_list = patterns.split(';') 
    # Collect input and output arguments into one bunch 
    class Bunch: 
        def __init__(self, **kwds): 
            self.__dict__.update(kwds) 

    arg = Bunch(recurse=recurse, pattern_list=pattern_list, 
        return_folders=return_folders, results=[]) 

    def visit(arg, dirname, files): 
        # Append to arg.results all relevant files (and perhaps folders) 
        for name in files: 
            fullname = os.path.normpath(os.path.join(dirname, name)) 
            if arg.return_folders or os.path.isfile(fullname): 
                for pattern in arg.pattern_list: 
                    if fnmatch.fnmatch(name, pattern): 
                        arg.results.append(fullname) 
                        break 
        # Block recursion if recursion was disallowed 
        if not arg.recurse: files[:]=[] 

    os.path.walk(root, visit, arg) 

    return arg.results

def getPortalType(doc):
    elem = doc.getElementsByTagName('cmf:type')[0]
    cmftype = str(elem.firstChild.nodeValue.strip())
    return cmftype

def checkPortalType(doc, type_name):
    if getPortalType(doc) == type_name:
        return True
    else:
        return False


href = re.compile(r'href="([^"]+)"')
src = re.compile(r'src="([^"]+)"')

SITE_URLS = [
    'http://somesite.com',
    'http://www.somesite.com/'
]

def isLocal(url):
    if url.startswith('http://') or url.startswith('file://'):
        for site in SITE_URLS:
            if url.startswith(site):
                return True
    else:
        return True
    return False

def getLinks(doc, field):
    try:
        elem = [i for i in doc.getElementsByTagName('field') if i.getAttribute('name') == field][0]
    except IndexError:
        return []
    text = elem.firstChild.nodeValue
    #urls = href.findall(text)
    urls = src.findall(text)
    urls = filter(isLocal, urls)

    return urls

def getLinkStats(dirname='.', prefix=None, verbose=False, sort_on_entry=False):
    entries = {}

    if prefix is not None:
        pflen = len(prefix)

    replace_sep = os.path.sep == '/' and False or True

    files = listFiles(dirname, patterns='.marshall.xml')
    for f in files:
        doc = minidom.parse(f)
        if not checkPortalType(doc, 'BlogEntry'):
            continue

        links = getLinks(doc, 'body')

        if prefix and f.startswith(prefix):
            f = f[pflen:]
        f = os.path.dirname(f)
        if replace_sep:
            f = f.replace('\\', '/')
        if links:
            entries[f] = links

    links = []
    for value in entries.values():
        links.extend(value)
    absolute = [i for i in links if '://' in i]
    absolute.sort()
    relative = [i for i in links if i not in absolute]
    relative.sort()

    print '%d total links' % len(links)
    if verbose:
        if sort_on_entry:
            print '%d absolute links' % len(absolute)
            print '%d relative links' % len(relative)
            keys = entries.keys()
            keys.sort()
            for k in keys:
                print k
                for i in entries[k]:
                    print '\t%s' % i
        else:
            print '%d absolute links' % len(absolute)
            for l in absolute:
                print '\t%s' % l
            print '%d relative links' % len(relative)
            for l in relative:
                print '\t%s' % l

    return entries

def getLostContentStats(dirname='.', prefix=None, verbose=False):
    entries = []

    if prefix is not None:
        pflen = len(prefix)

    replace_sep = os.path.sep == '/' and False or True

    files = listFiles(dirname, patterns='.marshall.xml')
    for f in files:
        doc = minidom.parse(f)
        if not checkPortalType(doc, 'BlogEntry'):
            continue
        entries.append(f)

    content = {}
    for e in entries:
        files = listFiles(os.path.dirname(e), patterns='.objects.xml')

        if prefix and e.startswith(prefix):
            e = e[pflen:]
        e = os.path.dirname(e)
        if replace_sep:
            e = e.replace('\\', '/')

        for f in files:
            doc = minidom.parse(f)
            for r in doc.getElementsByTagName('record'):
                item_path = '/'.join([e, r.firstChild.nodeValue])
                content.setdefault(r.getAttribute('type'), []).append(item_path)

    print "Lost content in blog entries under %s:" % dirname 
    count = 0
    keys = content.keys()
    keys.sort()
    for k in keys:
        l = len(content[k])
        count += l
        print "  %s: %s" % (k, l)
        if verbose:
            for p in content[k]:
                print '\t%s' % p
    print "%d total" % count

def getContentStats(dirname='.', prefix=None, verbose=False):
    content = {}

    if prefix is not None:
        pflen = len(prefix)

    replace_sep = os.path.sep == '/' and False or True

    files = listFiles(dirname, patterns='.marshall.xml')
    for f in files:
        doc = minidom.parse(f)
        cmftype = getPortalType(doc)

        if prefix and f.startswith(prefix):
            f = f[pflen:]
        f = os.path.dirname(f)
        if replace_sep:
            f = f.replace('\\', '/')

        content.setdefault(cmftype, []).append(f)

    print "Content under %s:" % dirname 
    count = 0
    keys = content.keys()
    keys.sort()
    for k in keys:
        l = len(content[k])
        count += l
        print "  %s: %s" % (k, l)
        if verbose:
            for p in content[k]:
                print '\t%s' % p
    print "%d total" % count

ACTIONS = {
    'all': getContentStats,
    'lost': getLostContentStats,
    'links': getLinkStats,
}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].split('-', 1)[0] in ACTIONS:
        action = sys.argv[1].split('-', 1)
        if len(action) > 1:
            action, mod = action
            verbose = 'v' in mod and True or False
            sort_on_entry = 's' in mod and True or False
        else:
            action = action[0]
            verbose = False
            sort_on_entry = False
    else:
        print "Need one of next action as argument: %s" % ACTIONS.keys()
        sys.exit(1)
    if len(sys.argv) > 2:
        path = sys.argv[2]
    else:
        path = '.'
    if len(sys.argv) > 3 :
        prefix = sys.argv[3]
    elif path != '.':
        prefix = path
    else:
        prefix = None

    start = time.time()

    if action == 'links':
        ACTIONS[action](path, prefix, verbose, sort_on_entry)
    else:
        ACTIONS[action](path, prefix, verbose)

    end = time.time()
    print "%d second elapsed" % (end-start, )
