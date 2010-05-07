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


function referencebrowser_openBrowser(path, fieldName, at_url, fieldRealName, currnode) {
    var url = path + '/referencebrowser_popup?fieldName=' + fieldName + '&fieldRealName=' + fieldRealName +'&at_url=' + at_url;

    var order_idx = getOrderIndex(currnode);
    if (order_idx)
        url = url + '&order_idx=' + order_idx;

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
function referencebrowser_setReference(widget_id, uid, label, multi, order_idx)
{
    // differentiate between the single and mulitselect widget
    // since the single widget has an extra label field.
    if (multi==0) {
        element=getOrderedElement(widget_id, order_idx);
        label_element=document.getElementById(widget_id + '_label');
        element.value=uid;
        if (label_element != null)
            label_element.value=label;
     }  else {
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


