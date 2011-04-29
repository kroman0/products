// Hide #portal-bounty-program container BEFORE it will be loaded
// This will be done only for browser with javascript support.
$("<style type='text/css'>#portal-bounty-program .hidden{display:none;}</style>").appendTo("head");

function getRandomSubset(array, choice_num) {
    // Return randomly selected *choice_num* elements from the array.
    // Solution is based on the Fisher-Yates (Knuth) algorithm
    // (http://en.wikipedia.org/wiki/Fisher–Yates_shuffle).
    if (array.length <= choice_num)
        return array;

    var tmp, current, top = array.length;
    for(top=array.length-1; top>array.length-choice_num; --top) {
	current = Math.floor(Math.random() * top);
	tmp = array[current];
	array[current] = array[top];
	array[top] = tmp;
    }
    return array.slice(array.length-choice_num,array.length)
};

$(document).ready(function() {
    $(getRandomSubset($("#portal-bounty-program ul li"), 5))
        .each(function(i, el){
            $(el).removeClass('hidden');
	})
});
