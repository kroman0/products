// tiles.js

var DEBUG = false, styles = "";

function getElementsByClassName(className, parentElement) {
    var result = new Array(),
    list = (parentElement || window.document.body).getElementsByTagName('*');
    if(list.length == 0) list = (parentElement || window.document.body).all;
    for(var i = 0; i < list.length; i++) {
        if(DEBUG) styles += '\n' + list[i].className;
        if(list[i].className.match(new RegExp('(^|\\s)' + className + '(\\s|$)'))) result[result.length] = list[i];
    }
    return result
};

function setTiles(){
    var tiles_elms = getElementsByClassName("tile", window.document)
    for(var i = 0; i < tiles_elms.length; i++) {
        var tiles_a = tiles_elms[i].getElementsByTagName('A');
        if(tiles_a.length > 0) tiles_elms[i].onclick = function(){
            location.href = this.getElementsByTagName('A')[0].href
            };
        if(DEBUG) styles += '\n' + tiles_elms[i].onclick;
    }
    if(DEBUG) window.alert(styles);
}

registerPloneFunction(setTiles);