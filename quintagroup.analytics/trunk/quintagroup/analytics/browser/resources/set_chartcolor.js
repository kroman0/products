function rgb2hex(rgb) {
    rgb = rgb.match(/^rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*(\d+))?\)$/);
    function hex(x) {
        return ("0" + parseInt(x).toString(16)).slice(-2);
    }
    return hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3]);
}

jq(document).ready(function (){
    rgb_colors = jq(jq('[class|=state]'));
    if (rgb_colors.length>0){
        hex_colors = new Array();
        jq.each(rgb_colors, function (index, value){
           rgb = jq(value).css('color');
           hex_colors.push(rgb2hex(rgb));
        });
        src = jq("#chart img").attr('src');
        new_src = src.replace(/chco=[^&]+/, 'chco='+hex_colors.join());
        jq("#chart img").attr('src', new_src);
     }
});

