// tiles.js

var DEBUG = false, message = "";

function getElementsByClassName(className, parentElement) {
    var result = new Array(),
        list = (parentElement || window.document.body).getElementsByTagName('*');
    if(list.length == 0) list = (parentElement || window.document.body).all;
    var class_re = new RegExp('(^|\\s)' + className + '(\\s|$)');
    for(var i = 0; i < list.length; i++) if(list[i].className.match(class_re)) result[result.length] = list[i];
    return result;
};

// browser compatibility functions
function add_Event(obj, evt, listener, captured) {
    if (!obj.addEventListener) obj.attachEvent('on'+evt, listener);
    else obj.addEventListener(evt, listener, captured);
}

function stopBubbling(e) {
    if(!e) window.event.cancelBubble=true;
    else (e.stopPropagation) ? e.stopPropagation() : e.cancelBubble=true;
}

function getPrimaryLink(list) {
    // get first a.primary element from the list
    // or just first element if no primary anchor is marked
    if(list.length == 0) return false;
    var primary = new RegExp('(^|\\s)' + 'primary' + '(\\s|$)');
    for(var i = 0; i < list.length; i++) if(primary.exec(list[i].className)) return list[i];
    return list[0];
}

function initTiles(){
    var tiles = getElementsByClassName("tile", window.document)
    for(var i = 0; i < tiles.length; i++) {
        var tile = tiles[i],
            hrefs = tile.getElementsByTagName('A');
        var a = getPrimaryLink(hrefs);
        if (a) {
            // adding styling for tiles
            tile.style.cursor='pointer';
            tile.tabIndex = 0;
            // adding event handling
            add_Event(tile, 'click',     new Function("e", "window.location='"+a.href+"';stopBubbling(e)"), false);
            add_Event(tile, 'mouseover', new Function("e", "window.status=  '"+a.href+"';stopBubbling(e)"), false);
            add_Event(tile, 'mouseout',      function( e ){ window.status=  '';          stopBubbling(e) }, false);
        }
    }
}

registerPloneFunction(initTiles);