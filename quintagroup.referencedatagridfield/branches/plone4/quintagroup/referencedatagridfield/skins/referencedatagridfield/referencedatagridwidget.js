// ReferenceDataGridField related functions

dataGridFieldFunctions.addReferenceDataGridRow = function(id) {
    /* Explitcly add row for given DataGridField,
           then update row content with reference popup
           functionality.

           @param id Archetypes field id for the widget

    */
	
    // Add row with own DataGridField method
    this.addRow(id);

    // Find active row and add overlay related processors for active row
    var active_row = jq("#datagridwidget-tbody-" + id + " tr#datagridwidget-row:last");
    jq(active_row).prepRefPopup();
}

dataGridFieldFunctions.addReferenceDataGridRowAfter = function(currnode) {
    /*
        Creates a new row before the clicked row with preparation of
	reference related overlay.
    */
	
    // add row with datagrid original method
    this.addRowAfter(currnode);
    // find active row
    var tbody = jq(currnode).parents("[id^=datagridwidget-tbody-]");
    var rows = jq("#datagridwidget-row", tbody);
    var curr_row = jq(currnode).parents("tr#datagridwidget-row");
    var active_row = rows[rows.index(curr_row)-1];
    // add overlay related processors for active row
    jq(active_row).prepRefPopup();
}

dataGridFieldFunctions.OriginalUpdateOrderIndex = dataGridFieldFunctions.updateOrderIndex;
dataGridFieldFunctions.updateOrderIndex = function (tbody) {
    var rows, tr, idx, ov, ov_id, under_idx, new_ov_id
    // update order index with original method
    this.OriginalUpdateOrderIndex(tbody);
    // Update overlay related attributes after rows index updating
    // for all datagridwidget rows
    rows = jq("#datagridwidget-row", tbody);
    for (var i=0; i<rows.length; ++i) {
        // get working row
        tr = rows[i];
	// Update overlay related tags attributes
	order_tag = jq("input[id^=orderindex__]", tr);
	idx = order_tag.attr("value");
        // Update rel attribute for overlay box
	ov = jq("input.addreference", tr);
	ov_id = ov.attr("rel");
	under_idx = ov_id.lastIndexOf("_");
        base_id = (under_idx >= 0)? ov_id.substring(0, under_idx): "#atrb";
	new_ov_id = base_id + "_" + idx;
	ov.attr("rel", new_ov_id);
        // Update target box id - it must be equal to rel attribute
	jq("div[id^=atrb_]", tr).attr("id", new_ov_id.substring(1) );
    }
    
}

// Service scripts used in referencebrowser.js

function setClassAttr(element, value) {
    if (element.className) {
        element.className = value
    } else {
        element.setAttribute("CLASS", value)
    } 
}

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
