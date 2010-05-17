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
