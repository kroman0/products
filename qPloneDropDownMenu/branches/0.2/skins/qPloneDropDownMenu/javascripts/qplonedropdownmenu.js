var gObj = {title:'',url:''}, gEditCancel = {}, gReorderingLi = null;

var myrules = {
  '#app .item_icon' : function(el){
    el.onclick = function(ev){
      var ev = ev?ev:window.event, li = Event.findElement(ev, 'LI');
      if (el.hasClassName('collapsed_icon')) {
        expandItem(li);
        reorderDisplaying(li,true);
      }
      else {
        collapseItem(li);
        reorderDisplaying(li, false);
      };
      Event.stop(ev);
      return false;
    }
  },
  '#app .reorder' : function(el){
    el.onclick = function(ev){
      var ev = ev?ev:window.event, li = Event.findElement(ev, 'LI'),
          ul = li.getElementsByTagName('UL')[0];
      if (getChildLis(ul).length > 1){
        isCollapsed(li)?expandItem(li):'';
        gReorderingLi = li;
        Element.addClassName(li, 'childsort');
        disableScreen('rootMenu', li);
      };
      Event.stop(ev);
      return false;
    }
  },
  '#app .tabslist li div.deleteHover' : function(el){
     if (el.attachEvent){
      if (!el.hovers) el.hovers = {};
      if (el.hovers['hover']) return;
      el.hovers['hover'] = true;
      el.attachEvent('onmouseover', function(){el.className += ' hover';});
      el.attachEvent('onmouseout',  function(){el.className = el.className.replace((new RegExp('\\s+hover')),'');});
     }
  },
  '#app .delete' : function(el){
    el.onclick = function(ev){
      var ev = ev?ev:window.event, li = Event.findElement(ev, 'LI'), path = $F(li.getElementsByTagName('INPUT')[0]),
          ul = Event.findElement(ev, 'UL'),
          parentLi = ul.parentNode.parentNode;
      new Ajax.Request('qpdm_delete',
        {parameters:'submenu_path='+path,
         onSuccess:function(request) {
           new Effect.Fade(li, {duration: 0.7, afterFinish: function(){
             Element.update(ul.parentNode, request.responseText);
             reorderDisplaying(parentLi, true);
             Behaviour.apply();
           }});
         },
         onFailure: function(request) {window.alert(getMes(request.responseText));}
        }
      );
      Event.stop(ev);
      return false;
    }
  },
//   '#app .tabslist dt.collapsibleHeader' : function(el){el.onclick = toggleCollapsible;},
  '.tabslist li span' : function(el){
    el.onclick = function(ev){
      var ev = ev?ev:window.event, li = Event.findElement(ev, 'LI'),
          inputs = li.getElementsByTagName('INPUT');
      gEditCancel[inputs[0].value] = [inputs[2].value, inputs[3].value];
      Element.classNames(li).set('childedit');
      inputs[2].focus();
      Event.stop(ev);
      return false;
    }
  },
  '.tabslist input.editsave' : function(el){
    el.onclick = function(ev){
      var ev = ev?ev:window.event, li = Event.findElement(ev, 'LI'),
          inputs = li.getElementsByTagName('INPUT'), path = inputs[0].value,
          title = $F(inputs[2]);
      if (/[^\s]/.test(title)) {
         new Ajax.Request('qpdm_edit',
           {parameters:'submenu_path='+path+'&'+Form.serialize(Event.findElement(ev, 'FORM')),
            onSuccess: function(request){
              Element.classNames(li).set('');
              li.id = 'tabslist_'+title;
              li.getElementsByTagName('SPAN')[0].update(title);
              Behaviour.apply();
           },
           onFailure: function(request){window.alert(getMes(request.responseText));}
          }
        );
      }
      else window.alert('Name is required!');
      Event.stop(ev);
      return false;
    }
  },
  '.tabslist input.editcancel' : function(el){
    el.onclick = function(ev){
      var ev = ev?ev:window.event, li = Event.findElement(ev, 'LI'),
          inputs = li.getElementsByTagName('INPUT');
      Element.classNames(li).set('');
      values = gEditCancel[inputs[0].value];
      inputs[2].value = values[0];
      inputs[3].value = values[1];
      Event.stop(ev);
      return false;
    }
  },
  '#app li input.acttitle' : function(el){
    el.onfocus = function(ev){
      var ev = ev?ev:window.event, li = Event.findElement(ev, 'LI');
      Element.classNames(li).add('childadd');
      Event.stop(ev);
      return false;
    };
  },
 '#app li .buttonadd' : function(el){
    el.onclick = function(ev){
      var ev = ev?ev:window.event, li = Event.findElement(ev, 'LI'), lis=[],
          inputs = li.getElementsByTagName('INPUT'), form = Event.findElement(ev, 'FORM');
      if ($F(inputs[1])){
        new Ajax.Request('qpdm_add',
          {parameters:'num='+getChildLis(li.parentNode).length+'&'+Form.serialize(form),
           onSuccess: function(request){
             var parentLi = Event.findElement(ev, 'UL').parentNode.parentNode;
             new Insertion.Before(li, request.responseText);
             Element.removeClassName(li, 'childadd');
             Form.reset(form);
             reorderDisplaying(parentLi, true);
             Behaviour.apply();
           },
           onFailure: function(request){window.alert(getMes(request.responseText));}
          }
        );
      }
      else window.alert('Title is required!');
      Event.stop(ev);
      return false;
    }
  },
  '#app li .buttoncancel' : function(el){
    el.onclick = function(ev){
      var ev = ev?ev:window.event, li = Event.findElement(ev, 'LI');
      Element.removeClassName(li, 'childadd');
      Form.reset(Event.findElement(ev, 'FORM'));
      Event.stop(ev);
      return false;
    }
  }
//   '#generated_tabs' : function(el){
//     el.onclick = function(ev){new Ajax.Request('qpt_setproperty', {parameters:'generated_tabs='+el.checked});}
//   }
};

Behaviour.register(myrules);

var globalHandlers = {
  onCreate: function(){Element.addClassName('app', 'working');},
  onComplete: function() {if(Ajax.activeRequestCount == 0) Element.removeClassName('app', 'working');}
};

Ajax.Responders.register(globalHandlers);

function removeHandlers(el, cur) {
  var el = el?el:'rootMenu';
  getChildLis(el).each(function(item){item!=cur?item.getElementsByTagName('SPAN')[0].onclick='':'';});
};

function getMes(txt) {
  try {
    message = (/Error Value\s*<\/dt>\s*<dd>(.*?)<\/dd>/i).exec(txt)[1];
  }
  catch(e) {
    message = txt;
  };
  return message;
};

function collapseItem(item) {
  var img = document.getElementsByClassName('item_icon', item)[0],
      ul  = document.getElementsByClassName('tabslist', item)[0];
  if (img && ul){
    shiftClasses(img, 'expanded_icon', 'collapsed_icon');
    shiftClasses(ul, 'showLevel', 'hideLevel');
    return true;
  }
  else return false;
};

function expandItem(item) {
  var img = document.getElementsByClassName('item_icon', item)[0],
      ul  = document.getElementsByClassName('tabslist', item)[0];
  if (img && ul){
    shiftClasses(img, 'collapsed_icon', 'expanded_icon');
    shiftClasses(ul, 'hideLevel', 'showLevel');
    return true;
  }
  else return false;
};

function isCollapsed(item) {
    var ul = document.getElementsByClassName('tabslist', item);
  return (ul[0] && Element.hasClassName(ul[0], 'hideLevel'));
};

function initLightbox (li) {
  var objBody = document.getElementsByTagName("body").item(0),
      objOverlay = document.createElement("div"),
      objLi = document.createElement("li");
  objOverlay.setAttribute('id', 'overlay_modal');
  objLi.setAttribute('id', 'overlay_li');
  objOverlay.className = "overlay_alert";
  objLi.className = "overlay_li childsort";
  objOverlay.style.display = 'none';
  objLi.style.display = 'none';
  objOverlay.style.position = 'absolute';
  objLi.style.position = 'absolute';
  objOverlay.style.zIndex = 5000;
  objLi.style.zIndex = 10000;
  objOverlay.style.width = '100%';
  objLi.style.width = '100%';
  Element.update(objLi, li.innerHTML);
  objBody.insertBefore(objOverlay, objBody.firstChild);
  li.parentNode.appendChild(objLi);
};

function disableScreen(overElement, li) {
  initLightbox(li);
  var objOverlay = $('overlay_modal'), objLi = $('overlay_li'),
      ul = objLi.getElementsByTagName('UL')[0];
  Position.clone(overElement, objOverlay);
  Position.clone(li, objLi);
  objOverlay.style.display = 'block';
  objLi.style.display = 'block';
  ul ? Sortable.create(ul, {handle: 'drag-handle'}) : '';
  Event.observe(document.getElementsByClassName('cancel', objLi)[0], 'click', onReorderingCancel, false);
  Event.observe(document.getElementsByClassName('save', objLi)[0], 'click', onReorderingSave, false);
  return li;
};

function enableScreen(ev) {
  var ev = ev?ev:window.event, objOverlay =  $('overlay_modal'), objLi = $('overlay_li');
  Event.stopObserving(Event.element(ev), 'click', onReorderingCancel, false);
  Event.stopObserving(Event.element(ev), 'click', onReorderingSave, false);
  Sortable.destroy(objLi.getElementsByTagName('UL')[0]);
  if (objOverlay) Element.remove(objOverlay);
  if (objLi) Element.remove(objLi);
};

function getChildLis(el) {
  return $A($(el).childNodes).findAll(function(item){return (item.tagName=='LI'&&!Element.hasClassName(item,'addItem'))})
};

function reorderDisplaying(el, expand) {
  var div = el.getElementsByTagName('DIV')[0],
      lis = getChildLis(el.getElementsByTagName('UL')[0]).length;;
  if (expand && lis>1) Element.addClassName(div, 'reorderHover');
  else Element.removeClassName(div, 'reorderHover');
};

function shiftClasses(el, from, to) {
  Element.removeClassName(el, from);
  Element.addClassName(el, to);
};

function onReorderingCancel(ev) {
  var ev = ev?ev:window.event, ul = gReorderingLi.getElementsByTagName('UL')[0];
  if (ul) {
    Element.removeClassName(gReorderingLi, 'childsort');
    enableScreen(ev);
  };
  Event.stop(ev);
  return false;
};

function onReorderingSave(ev) {
  var ev = ev?ev:window.event, li = Event.findElement(ev, 'LI'),
      path = li.getElementsByTagName('INPUT')[0].value,
      ul = li.getElementsByTagName('UL')[0], params = '',
      ulOrigin = gReorderingLi.getElementsByTagName('UL')[0];
  $A(getChildLis(ul)).each(function(i){
    var val = i.getElementsByTagName('INPUT')[1].value;
    params += val?'&idxs='+val:'';
  });
  new Ajax.Request('qpdm_reorder',
    {method: 'post',
     parameters: 'submenu_path='+path+params,
     onSuccess: function(request){
       new Effect.Highlight(ulOrigin, {duration: 0.7, afterFinish: function(){
       Element.removeClassName(gReorderingLi, 'childsort');
       Element.update(ulOrigin.parentNode, request.responseText);
       enableScreen(ev);
       Behaviour.apply();}});
     },
    onFailure: function(request){window.alert(getMes(request.responseText));},
    }
  );
  Event.stop(ev);
  return false;
}
