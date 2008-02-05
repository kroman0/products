## Script (Python) "switchOverlays"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

return """
<script type="text/javascript">
//<![CDATA[

function getData(){
  var ul = document.getElementById('listOverlays'),  result = {};
  if ((ul != null) && (ul.getElementsByTagName('INPUT').length > 0)) {
    var boxes = ul.getElementsByTagName('INPUT');
    result['boxes'] = boxes;
    for (var i=0; i < boxes.length; i++) result[boxes[i].id.replace(/Box$/, '')] = boxes[i].checked;
  }
  else return false;
  return result
};

registerEventListener(window, 'unload', GUnload);

//]]>
</script>
"""