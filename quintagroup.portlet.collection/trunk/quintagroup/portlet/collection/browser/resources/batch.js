jq(document).ready(function(e) {
    var prev_link = jq('.prevlink');
    var next_link = jq('.nextlink');
    var nav_links = jq('.navlink');
    var batch_size = 4;
    batch_size = nav_links.size() > batch_size ? batch_size : nav_links.size();

    var hideNavigation = function (){
      jq.each(nav_links, function(index, link){
        jq(link).hide();
      });
    };

    var showPageByIndex = function(index){
      jq('dd[class*=page]').hide();
      jq('dd.page-'+(index)).show();
    };

    var bind_prev_handler = function(link, index){
      if (index == 0) jq(link).hide();
      jq(link).unbind();
      jq(link).click(function(e) {
        if (!(index % batch_size)) {
          hideNavigation();
          for (i=1;i<=batch_size;i++){
            jq(nav_links[index-i]).show();
          }
        }
        nav_link_handler(index-1);
     });
    };
    var bind_next_handler = function(link, index){
      if (index == nav_links.size()-1) jq(link).hide();
      jq(link).unbind();
      jq(link).click(function(e) {
        if (!((index+1) % batch_size)) {
          hideNavigation();
          for (i=1;i<=batch_size;i++){
            if (i+index<nav_links.size()){
              jq(nav_links[i+index]).show();
            }
            if (i==batch_size) {
              jq(nav_links[i+index]).find('.navlinkSeparator').hide();
            }
          }
        }
        nav_link_handler(index+1);
      });
    };
    var nav_link_handler = function(index){
      if (index > 0) {
        prev_link.show();
        bind_prev_handler(prev_link, index);
      }
      else {
        prev_link.hide();
      }
      if (index < nav_links.size()-1) {
        next_link.show();
        bind_next_handler(next_link, index);
      }
      else {
        next_link.hide();
      }
      showPageByIndex(index);
      for (i=0;i<nav_links.size();i++){
        if (i == index) {
          jq(nav_links[i]).addClass('selected');
        }
        else{
          jq(nav_links[i]).removeClass('selected');
      }
      }
    }
    var initialize_navigation = function(){
      prev_link.show();
      next_link.show();
      for (i=0; i<batch_size;i++){
          jq(nav_links[i]).show();
          if (i==batch_size-1) {
            jq(nav_links[i]).find('.navlinkSeparator').hide();
          }
      }
      showPageByIndex(0);
      bind_prev_handler(prev_link, 0);
      bind_next_handler(next_link, 0);
      jq.each(nav_links, function(index, link) {
        jq(link).unbind();
        jq(link).click(function(e) {
          nav_link_handler(index);
        });
    });
    };

   initialize_navigation();

});
