// Crossbrowser event listeners adder
function addEvent(obj, evType, fn, useCap) {
    var r = false;
    if (obj.addEventListener){
        if (typeof(useCap) == 'undefined')
	    useCap = false;
        obj.addEventListener(evType, fn, useCap);
        r = true;
     }
     else if (obj.attachEvent) {
	 var id = obj.sourceIndex || -1;

	 if (!fn[evType + id]) {
	     var f = fn[evType + id] = function(e) {
		 var o = document.all[id] || document;
		 o._f = fn;
		 var s = o._f(e);
		 o._f = null;
		 return s;
	     };

	     r = obj.attachEvent("on" + evType, f);
	     obj = null;
	 }
     }
     return r;
 };

function triggerTitleClass(e) {
    var currnode = window.event ? window.event.srcElement : e.currentTarget;
    
	// fetch required data structure   
    var element = getThisOrParentElement(currnode, "INPUT");
    // If no input tag found - leave function
    if (element == null || element.tagName.toUpperCase() == "BODY")
	return;
    
    var current = element.value;
    var initial = element.getAttribute("default_value");
    if (initial == null || current == null)
	return;

    if (initial == current) {
       setClassAttr(element, "not-changed-title-field")
    } else {
       setClassAttr(element, "changed-title-field")
    }
}

function setClassAttr(element, value) {
    if (element.className) {
        element.className = value
    } else {
        element.setAttribute("CLASS", value)
    } 
}
// Trigger styles on focusing on the element
function triggerOnFocusStyles(e) {
    var currnode = window.event ? window.event.srcElement : e.currentTarget;
    
	// fetch required data structure   
    var element = getThisOrParentElement(currnode, "INPUT");
    // If no input tag found - leave function
    if (element == null || element.tagName.toUpperCase() == "BODY")
	return;
    setClassAttr(element, "changed-title-field")
}

function getThisOrParentElement(currnode, tagname) {
    /* Find the first parent node with the given tag name */

    tagname = tagname.toUpperCase();
    var parent = currnode;

    while(parent.tagName.toUpperCase() != tagname) {
        parent = parent.parentNode;
        // Next line is a safety belt
        if(parent.tagName.toUpperCase() == "BODY") 
            return null;
    }

    return parent;
}


// function to open the popup window
function getOrderIndex(currnode) {
    if (typeof(dataGridFieldFunctions) == "object") {
        var rows = dataGridFieldFunctions.getWidgetRows(currnode);
	var row = dataGridFieldFunctions.getParentElementById(currnode, "datagridwidget-row");      
	if(row == null) {
	    alert("Couldn't find DataGridWidget row");
	    return;
	}

	var idx = null

	// We can't use nextSibling because of blank text nodes in some browsers
	// Need to find the index of the row
	for(var t = 0; t < rows.length; t++) {
	    if(rows[t] == row) {
		idx = t;
		break;
	    }
	}

	// Abort if the current row wasn't found
	if(idx == null)
	    return;
        return idx;
    }
    return;
}

function getOrderedElement(widget_id, order_idx) {
    // First get first element for the current field
    var element=document.getElementById(widget_id);

    // If it is about DataGridField use it to chose correct element
    if (typeof(dataGridFieldFunctions) == "object" && order_idx >= 0) {
        var rows = dataGridFieldFunctions.getWidgetRows(element);
        if (rows.length >= order_idx) {
            var row = rows[order_idx]
            var inputs = row.getElementsByTagName("input")
            for (var i=0;i<=inputs.length;i++) {
		if (inputs[i].id == widget_id) {
		    element = inputs[i];
                    break;
		}
            }
        }
    }
    return element;
}


function referencedatagridbrowser_openBrowser(path, fieldName, at_url, fieldRealName, fieldTitleName, fieldLinkName, currnode) {
    var url = path + '/referencebrowser_popup?fieldName=' + fieldName + '&fieldRealName=' + fieldRealName +'&at_url=' + at_url;

    var order_idx = getOrderIndex(currnode);
    url += (typeof(order_idx) == 'number')? '&order_idx=' + order_idx: "";
    url += (typeof(fieldTitleName) != 'undefined')? '&fieldTitleName=' + fieldTitleName: "";
    url += (typeof(fieldLinkName) != 'undefined')? '&fieldLinkName=' + fieldLinkName: "";

    atrefpopup = window.open(url, 'referencebrowser_popup','toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=500,height=550');
}

// function for Array detecting
function typeOf(value) {
    var s = typeof value;
    if (s === 'object') {
        if (value) {
            if (value instanceof Array) {
                s = 'array';
            }
        } else {
            s = 'null';
        }
    }
    return s;
}

// function to return a reference from the popup window back into the widget
function referencedatagridbrowser_setReference(widget_id, uid, label, multi, order_idx, widget_title_id, link_title, widget_link_id, link_path)
{
    if (order_idx >= 0) {
        // process ReferenceDataGridField
        uid_element=getOrderedElement(widget_id, order_idx);
        uid_element.value=uid;
        title_element=getOrderedElement(widget_title_id, order_idx);
        title_element.value=link_title;
        title_element.className="not-changed-title-field";
        title_element.setAttribute("default_value", link_title);
        addEvent(title_element, 'blur', triggerTitleClass, false)
        addEvent(title_element, 'focus', triggerOnFocusStyles, false)
        link_element=getOrderedElement(widget_link_id, order_idx);
        link_element.readOnly=false;
        link_element.value=link_path;
        link_element.readOnly=true;
        link_element.className="hidden-field"
    } else if (multi==0) {
	// differentiate between the single and mulitselect widget
	// since the single widget has an extra label field.
        element=document.getElementById(widget_id);
        label_element=document.getElementById(widget_id + '_label');
        element.value=uid;
        label_element.value=label;
    } else {
         // check if the item isn't already in the list
         var current_values = cssQuery('#' + widget_id + ' input');
         for (var i=0; i < current_values.length; i++) {
            if (current_values[i].value == uid) {
              return false;
            }
          }         
          // now add the new item
          list=document.getElementById(widget_id);
          li = document.createElement('li');
          label_element = document.createElement('label');
          input = document.createElement('input');
          input.type = 'checkbox';
          input.value = uid;
          input.checked = true;
          input.name = widget_id + ':list';
          label_element.appendChild(input);
          label_element.appendChild(document.createTextNode(label));
          li.appendChild(label_element);
          list.appendChild(li);
          // fix on IE7 - check *after* adding to DOM
          input.checked = true;
    }
}

// function to clear the reference field or remove items
// from the multivalued reference list.
function referencebrowser_removeReference(widget_id, multi)
{
    if (multi) {
        list=document.getElementById(widget_id)
        for (var x=list.length-1; x >= 0; x--) {
          if (list[x].selected) {
            list[x]=null;
          }
        }
        for (var x=0; x < list.length; x++) {
            list[x].selected='selected';
          }        
    } else {
        element=document.getElementById(widget_id);
        label_element=document.getElementById(widget_id + '_label');
        label_element.value = "";
        element.value="";
    }
}


