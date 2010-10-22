$(document).ready(function() {
    $('.portletPFG .ArchetypesStringWidget').each(function(){$('input',this).attr('title',$('label',this).text()).addClass('inputLabel')})
});
