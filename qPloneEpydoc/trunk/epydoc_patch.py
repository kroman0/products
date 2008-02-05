# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2005-11-23 12:35:02
# Copyright: quintagroup.com

"""
This module contain fixed functions from epydoc classes that have to replace original.
"""
from epydoc.uid import UID, Link, make_uid, findUID
from epydoc.objdoc import ObjDoc, _find_base_order, _lookup_class_field, Var
from epydoc.uid import _ZopeType, _ZopeMethodType, _ZopeCMethodType
from epydoc.cli import _internal_error
import epydoc.markup as markup
import sys, os.path, re, getopt, types
from epydoc.cli import _Progress
import epydoc.cli
import epydoc.html
import epydoc.objdoc

def epydoc_html_write_breadcrumbs(self, public, private, where=None):
        """
        Write the HTML code for the breadcrumbs line to the given
        streams.  The breadcrumbs line is an invisible table with a
        list of pointers to the current object's ancestors on the
        left; and the show/hide private selector and the
        frames/noframes selector on the right.

        @param where: An identifier indicating what page we're
            creating a navigation bar for.  This is either a UID
            (for an object documentation page); or a string.  If
            it is a UID, then a list of pointers to its ancestors
            is displayed.
        @param public: The output stream for the public version of the page.
        @param private: The output stream for the private version of the page.
        """
        # Write the breadcrumbs (pointers to ancestors)
        str = '<table width="100%" cellpadding="0" cellspacing="0">\n'
        str += '  <tr valign="top">\n    <td width="100%">\n'
        if isinstance(where, UID): str += self._breadcrumbs(where)
        str += '    </td>\n    <td>'
        str += '<table cellpadding="0" cellspacing="0">\n'
        public.write(str); private.write(str)

        # Write the public/private link
        if self._create_private_docs:
            link = self._public_private_link(where, from_private=0)
            public.write('      <tr><td align="right">%s</td></tr>\n' % link)
            link = self._public_private_link(where, from_private=1)
            private.write('      <tr><td align="right">%s</td></tr>\n' % link)

        # Write the frames/noframes link.
        frames_link = ""
        if self._frames_index:
            frames_link = self._frames_link(where)
        str = ('      <tr><td align="right">%s</td></tr>\n' % frames_link)
        str += '    </table></td>\n'
        str += '</tr></table>\n'
        public.write(str); private.write(str)

def epydoc_object__init__(self, uid, verbosity=0):
        cls = uid.value()
        # Variables:
        self._tmp_ivar = {}
        self._tmp_cvar = {}
        self._tmp_type = {}
        self._property_type = {}

        ObjDoc.__init__(self, uid, verbosity)

        # Handle methods & class variables
        self._methods = []
        self._cvariables = []
        self._ivariables = []
        self._staticmethods = []
        self._classmethods = []
        self._properties = []

        # Find the order that bases are searched in.
        base_order =  _find_base_order(cls)
        self._base_order = [make_uid(b) for b in base_order]

        try: fields = dir(cls)
        except: fields = []
        for field in fields:
            # Don't do anything for these special variables:
            # this is fenix changes
            docstring = ''
            try:
                docstring = getattr(cls, field).__doc__
            except:
                pass
            if field in ('__doc__', '__module__', '__dict__',
                         '__weakref__', '__basicnew__', '__reduce__','__repr__')\
            or (not field.startswith('__') and docstring in ( "PermissionRole",
                                                              "Default Accessor.",
                                                              "Default Mutator.",
                                                              "Default Edit Accessor."
                                                            )):
                continue

            # Find the class that defines the field; and get the value
            # directly from that class (so methods & variables have
            # the right uids).
            (val, container) = _lookup_class_field(cls, field, base_order)

            linkname = field
            private_prefix = '_%s__' % container.shortname()
            if field.startswith(private_prefix):
                if container == self._uid:
                    # If it's private and belongs to this class, then
                    # undo the private name mangling.
                    linkname = linkname[len(private_prefix)-2:]
                else:
                    # If it's private, and belongs to a parent class,
                    # then don't even list it here.
                    continue

            # Deal with static/class methods and properties. (Python 2.2)
            try:
                # Get the un-munged value.
                try: rawval = container.value().__dict__.get(field)
                except: pass

                if isinstance(rawval, staticmethod):
                    vuid = make_uid(rawval, container, linkname)
                    vlink = Link(linkname, vuid)
                    self._staticmethods.append(vlink)
                    continue
                elif isinstance(rawval, classmethod):
                    vuid = make_uid(rawval, container, linkname)
                    vlink = Link(linkname, vuid)
                    self._classmethods.append(vlink)
                    continue
                elif isinstance(rawval, property):
                    vuid = make_uid(rawval, container, linkname)
                    vlink = Link(linkname, vuid)
                    self._properties.append(vlink)
                    continue
            except NameError: pass

            # Create a UID and Link for the field value.
            vuid = make_uid(val, container, linkname)
            vlink = Link(linkname, vuid)

            # Don't do anything if it doesn't have a full-path UID.
            if vuid is None: continue
            # Don't do anything for modules.
            if vuid.is_module(): continue

            # Is it a method?
            if vuid.is_routine():
                self._methods.append(vlink)

            elif container == self._uid:
                # Is it an instance variable?
                if self._tmp_ivar.has_key(field):
                    descr = self._tmp_ivar[field]
                    del self._tmp_ivar[field]
                    typ = self._tmp_type.get(field)
                    if typ is not None: del self._tmp_type[field]
                    else: typ = markup.parse_type_of(val)
                    self._ivariables.append(Var(field, vuid, descr, typ, 1))

                # Is it a class variable?
                else:
                    autogen = 1 # is it autogenerated?
                    descr = self._tmp_cvar.get(field)
                    if descr is not None:
                        del self._tmp_cvar[field]
                        autogen = 0
                    typ = self._tmp_type.get(field)
                    if typ is not None:
                        del self._tmp_type[field]
                        autogen = 0
                    else: typ = markup.parse_type_of(val)
                    self._cvariables.append(Var(field, vuid, descr,
                                                typ, 1, autogen))

        # Keep track of types for properties.
        for prop in self._properties:
            name = prop.name()
            typ = self._tmp_type.get(name)
            if typ is not None:
                if prop.target().cls() != self._uid:
                    estr = "@type can't be used on an inherited properties"
                    self._field_warnings.append(estr)
                self._property_type[prop.target()] = typ
                del self._tmp_type[name]

        # Add the remaining class variables
        for (name, descr) in self._tmp_cvar.items():
            typ = self._tmp_type.get(name)
            if typ is not None: del self._tmp_type[name]
            vuid = make_uid(None, self._uid, name)
            self._cvariables.append(Var(name, vuid, descr, typ, 0))

        # Add the instance variables.
        for (name, descr) in self._tmp_ivar.items():
            typ = self._tmp_type.get(name)
            if typ is not None: del self._tmp_type[name]
            vuid = make_uid(None, self._uid, name)
            self._ivariables.append(Var(name, vuid, descr, typ, 0))

        # Make sure we used all the type fields.
        if self._tmp_type:
            for key in self._tmp_type.keys():
                estr = '@type for unknown variable %s' % key
                self._field_warnings.append(estr)
        del self._tmp_ivar
        del self._tmp_cvar
        del self._tmp_type

        # Add links to base classes.
        try: bases = cls.__bases__
        except AttributeError: bases = []
        self._bases = [Link(base.__name__, make_uid(base)) for base in bases
                       if (type(base) in (types.ClassType, _ZopeType) or
                           (isinstance(base, types.TypeType)))]

        # Initialize subclass list.  (Subclasses get added
        # externally with add_subclass())
        self._subclasses = []

        # Is it an exception?
        try: self._is_exception = issubclass(cls, Exception)
        except TypeError: self._is_exception = 0

        # Inherited variables (added externally with inherit())
        self._inh_cvariables = []
        self._inh_ivariables = []

        # Assemble a list of all methods
        self._allmethods = (self._methods) #XXX+ self._classmethods +
                            #self._staticmethods)

        # Put everything in sorted order.
        self._methods = self._sort(self._methods)
        self._classmethods = self._sort(self._classmethods)
        self._staticmethods = self._sort(self._staticmethods)
        self._properties = self._sort(self._properties)
        self._cvariables = self._sort(self._cvariables)
        self._ivariables = self._sort(self._ivariables)
        self._bases = self._sort(self._bases)
        self._subclasses = self._sort(self._subclasses)
        self._allmethods = self._sort(self._allmethods)

        # Print out any errors/warnings that we encountered.
        self._print_errors()

def epydoc_cli_make_docmap(modules, options):
    """
    Construct the documentation map for the given modules.

    @param modules: The modules that should be documented.
    @type modules: C{list} of C{Module}
    @param options: Options from the command-line arguments.
    @type options: C{dict}
    """
    from epydoc.objdoc import DocMap, report_param_mismatches

    verbosity = options['verbosity']
    document_bases = 0
    document_autogen_vars =1
    inheritance_groups = (options['inheritance'] == 'grouped')
    inherit_groups = (options['inheritance'] != 'grouped')
    d = DocMap(verbosity, document_bases, document_autogen_vars,
               inheritance_groups, inherit_groups)
    if options['verbosity'] > 0:
        print  >>sys.stderr, ('Building API documentation for %d modules.'
                              % len(modules))
    progress = _Progress('Building docs for', verbosity, len(modules))

    for module in modules:
        progress.report(module.__name__)
        # Add the module.  Catch any exceptions that get generated.
        try: d.add(module)
        except Exception, e:
            if options['debug']: raise
            else: _internal_error(e)
        except:
            if options['debug']: raise
            else: _internal_error()

    if not options['ignore_param_mismatch']:
        if not report_param_mismatches(d):
            estr = '    (To supress these warnings, '
            estr += 'use --ignore-param-mismatch)'
            print >>sys.stderr, estr

    return d

epydoc.cli._make_docmap = epydoc_cli_make_docmap
epydoc.html.HTMLFormatter._write_breadcrumbs = epydoc_html_write_breadcrumbs
epydoc.objdoc.ClassDoc.__init__ = epydoc_object__init__