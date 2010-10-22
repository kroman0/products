$(document).ready(function() {
    $('.portletPFG input[type=text]')
        .attr('onblur',"if(this.value == '')this.value=this.defaultValue;")
        .attr('onclick',"this.value = '';")
});
