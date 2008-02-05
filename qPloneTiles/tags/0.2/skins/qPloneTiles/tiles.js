// tiles.js

var DEBUG = false, message = "";

function getElementsByClassName(className, parentElement) {
    var result = new Array(),
        list = (parentElement || window.document.body).getElementsByTagName('*');
    if(list.length == 0) list = (parentElement || window.document.body).all;
    for(var i = 0; i < list.length; i++) {
//        if(DEBUG) message += '\n' + list[i].className;
        if(list[i].className.match(new RegExp('(^|\\s)' + className + '(\\s|$)'))) result[result.length] = list[i];
    }
    return result
};

function getNeededHref(a_list) {
    var result, classname_re = new RegExp('(^|\\s)' + 'primary' + '(\\s|$)');
    if(a_list.length == 0) return false;
    for(var i = 0; i < a_list.length; i++) {
        if(classname_re.exec(a_list[i].className)) return a_list[i].href;
    }
    return a_list[0].href
}

function setTiles(){
    var tiles_elms = getElementsByClassName("tile", window.document)
    for(var i = 0; i < tiles_elms.length; i++) {
        var tiles_a = tiles_elms[i].getElementsByTagName('A');
        if(tiles_a.length > 0) {
            var Href = getNeededHref(tiles_a);
            if(Href != false) tiles_elms[i].onclick = new Function("window.location = '"+Href+"'; return false;")
            }
        if(DEBUG) message += '\n' + tiles_elms[i].onclick + ' - ' + Href;
    }
    if(DEBUG) window.alert(message);
}

registerPloneFunction(setTiles);