// ReferenceDataGridField related functions

dataGridFieldFunctions.addReferenceDataGridRow = function(id) {
    /* Explitcly add row for given DataGridField,
           then update row content with reference popup
           functionality.

           @param id Archetypes field id for the widget

    */
	
    // Add row with own DataGridField method
    this.addRow(id);
    // Find adde row - row before last one
    var tbody = document.getElementById("datagridwidget-tbody-" + id);
    var rows = this.getRows(tbody);
    var preLastRow = rows[rows.length-2];
    // Update row with Reference popup functionality
    jq(preLastRow).prepRefPopup();
}
