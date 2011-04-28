// Hide #portal-bounty-program container BEFORE it will be loaded
// This willbe done only for browser with javascript support.
$("<style type='text/css'>#portal-bounty-program .hidden{display:none;}</style>").appendTo("head");

function getRandomSubset(array, choice_num) {
    // Return randomly selected *choice_num* elements from the array
    var tmp, current, top = array.length;
    if (array.length > choice_num) {
	// random elements places to the end of the array
	for(top=array.length-1; top>array.length-choice_num; --top) {
	    current = Math.floor(Math.random() * top);
	    tmp = array[current];
	    array[current] = array[top];
	    array[top] = tmp;
	}
	return array.slice(array.length-choice_num,array.length)
    } else {
        return array;
    }
};

$(document).ready(function() {
    $(getRandomSubset($("#portal-bounty-program ul li"), 5))
        .each(function(i, el){
            $(el).removeClass('hidden');
	})
});
