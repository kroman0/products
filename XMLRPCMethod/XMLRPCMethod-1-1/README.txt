XMLRPC Methods

  The XMLRPC Method product provides support for remote procedure
  calls with the "XML-RPC":http://www.xml-rpc.com standard.
  The intent is to create a plug-in replacement for an external method.

  Not everything is callable: For instance you can't call title or id
  on a folder, but you can call 'title_or_id', 'title_and_id', 'getId'
  and 'getPhysicalPath'. Essentially everything that will also work as
  'http://remote.com/folder/title_or_id'. The method 'propertyItems' returns
  an especially complex and interesting result.

  You can also do privileged things that requires a login. You simply
  add the username and password to the remote url the conventional way:

    http://username:password@remote.com/

  Then you can call methods such as 'document_src' on DTML methods etc.

Sending arguments

  XMLRPC allows you to send a number of arguments to the remote
  procedure. These arguments can be integers, strings, lists, dictionaries
  etc. and combinations hereof.

  To test with the XMLRPCLIB example, create a XMLRPC method with the
  name 'statelookup', the URL 'http://betty.userland.com' and the method
  'examples.getStateName'.

  The create a DTML method with the call: '<dtml-var "statelookup(5)">'
  and see what happens.

Sending arguments to remote DTML Methods

  Try this: create a DTML method with address /welcome on the remote
  computer with the two lines::

    <dtml-call "REQUEST.set('res', 'Welcome to ' + place )">
    <dtml-return "REQUEST['res']">

  Then on the local computer create an XMLRPC method called querywelcome
  with the URL http://remote.com/, and a method of welcome.

  To call the remote procedure from a DTML Method do::

    <dtml-var "querywelcome( {'place':'my world'}) ">

  If the method returns a list or a dictionary, you can use the &lt;dtml-in *method* mapping>
 
Calling a Z SQL Method:

  You can't do it directly. The Z SQL Method returns objects, so you
  must use a DTML Method to build a list of dictionaries. Let's assume
  we have a table with the two columns 'ISSUE_ID' and 'ISSUE_NAME'. Then
  your DTML Method will look like this::

    <dtml-call "REQUEST.set('result',[])">
    <dtml-in select_all_from_issues>
    <dtml-call "REQUEST['result'].append({'ID': ISSUE_ID, 'NAME':ISSUE_NAME}) ">
    </dtml-in>
    <dtml-return "REQUEST['result']">

Other things to note:

  When an object is called via XML-RPC, there's nothing in the REQUEST
  variable. You can create variables in the namespace, but that's it. Some
  versions of Zope can't see simple variables.  So in the example above you
  have to write '<dtml-return "REQUEST[&apos;result&apos;]">' rather than
  '<dtml-return result>' to be one the safe side.

  Due to its nature XMLRPC methods can take a long time to execute or
  not return at all if the remote server is unresponsive. Therefore make
  use of the timeout value. The timeout functionality is implemented
  with threads.

  Another optimization technique available to you is to cache the results.
  We have made XMLRPCMethod cacheable with RAMCacheManager.

Bugs

  XML-RPC takes only positional parameters. Since arguments given in
  the 'QUERY_STRING' are keyword arguments as in ?x=1&amp;y=2
  it isn't possible to specify arguments in GET or POST statements.

  The &lt;dateTime.iso8601&gt; element is difficult to use. It is not
  converted to a Zope DateTime.

References

  "Directory of services":http://www.xmlrpc.com/directory/1568/services
