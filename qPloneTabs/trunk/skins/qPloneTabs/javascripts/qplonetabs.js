/* Global variables */

var gBeforeReorderFragment = null;  // document fragment for insertion in UL after clicking cancel button after reorder
var gBeforeEditData = {};  // hash for storage tabs fields before editing
var category = 'portal_tabs';

/* Main part - rules for element on our form */

var myrules = {
  '#app #reorder' : function(el){
    el.onclick = function(ev){
      var ev = ev?ev:window.event;
      gBeforeReorderFragment = document.getElementById('tabslist').innerHTML;
      shiftClassNames('app', 'viewing', 'sorting');
      Sortable.create('tabslist', {handle: 'drag-handle'});
      removeEdition('tabslist');
      Event.stop(ev);
      return false;
    }
  },
  '#app #save' : function(el){
    el.onclick = function(ev){
      var ev = ev?ev:window.event, params = 'category='+category;
      $A($('tabslist').getElementsByTagName('INPUT')).findAll(function(h){return h.type=='hidden';}).each(function(f,idx){params += '&idxs='+f.value;});
      new Ajax.Request('qpt_reorder',
        {method: 'post',
         parameters: params,
         onSuccess: function(request){
           var lis = $A($('tabslist').getElementsByTagName('LI')),
               inputs = function(li){return $A(li.getElementsByTagName('INPUT'))};
           lis.each(function(el,idx){
             inputs(el).each(function(inpt){
               inpt.type=='hidden'?inpt.value=idx:inpt.name=inpt.name.replace(/i\d+_/, 'i'+idx+'_');
             });
           });
           shiftClassNames('app', 'sorting', 'viewing');
           Sortable.destroy('tabslist');
           new Effect.Highlight('tabslist',{});
         },
         onComplete: function(request){Behaviour.apply();}
        }
      );
      Event.stop(ev);
      return false;
    }
  },
  '#app #cancel' : function(el){
    el.onclick = function(ev){
      var ev = ev?ev:window.event;
      Sortable.destroy('tabslist');
      shiftClassNames('app', 'sorting', 'viewing');
      Element.update('tabslist', gBeforeReorderFragment);
      el.attachEvent ? ieHover():'';
      Behaviour.apply();
      Event.stop(ev);
      return false;
    }
  },
  '#app .csshover li' : function(el){
    if (Element.hasClassName(el, 'onHover')) {Element.removeClassName(el, 'onHover');};
  },
  '#app .visibility' : function(el){
    el.onclick = function(ev) {
      var ev = ev?ev:window.event, li = Event.findElement(ev, 'LI'),
          num = $A($('tabslist').getElementsByTagName('LI')).indexOf(li),
          params = {
            onSuccess: function(request){
              if (Element.hasClassName(li, 'invisible')) {
                Element.removeClassName(li, 'invisible');
              }
              else {
                Element.addClassName(li, 'invisible');
              };
            },
            onFailure: function(request){
              var message = (/Error Value\s*<\/dt>\s*<dd>(.*?)<\/dd>/i).exec(request.responseText);
              window.alert(message[1]);
            }
          };
      if (Event.findElement(ev, 'UL').id == 'roottabs'){
        params['parameters'] = 'id='+el.id+'&visibility='+el.checked;
        new Ajax.Request('qpt_setvisibility', params);
      }
      else {
        params['parameters'] = 'category='+category+'&num='+num+'&visibility='+el.checked+'&'+Form.serialize(li.getElementsByTagName('FORM')[0]);
        new Ajax.Request('qpt_edit', params);
      };
      if (ev.stopPropagation) {ev.stopPropagation();}
      else {ev.cancelBubble = true;};
      return true;
    }
  },
  '#app .delete' : function(el){
    el.onclick = function(ev){
      var ev = ev?ev:window.event, item = el.parentNode,
          num = $A($('tabslist').getElementsByTagName('LI')).indexOf(item);
      new Ajax.Request('qpt_delete',
        {parameters:'category='+category+'&idx='+num+'&id=' + item.id.replace('tabslist_', ''),
         onComplete: function(request) {
           new Effect.Fade(item, {duration: 0.3, afterFinish: function(){
             Element.remove(item);
             var lis = $A($('tabslist').getElementsByTagName('LI')),
                 inputs = function(li){return $A(li.getElementsByTagName('INPUT'))};
             if (lis.length > 0) {
               lis.each(function(el,idx){
                 inputs(el).each(function(inpt){
                   inpt.type=='hidden'?inpt.value=idx:inpt.name=inpt.name.replace(/i\d+_/, 'i'+idx+'_');
                 });
               });
             } else {
                 Element.addClassName('reorder', 'noitems');
             };
           }});
         }
        }
      );
      Event.stop(ev);
      return false;
    }
  },
  '#app .headerAdvanced' : function(el){
    el.onclick =  function(ev){
      var ev = ev?ev:window.event, dl = Event.findElement(ev, 'DL'),
          dd = dl.getElementsByTagName('DD')[0];
      if (!Element.visible(dd)) {
        shiftClassNames(dl, 'collapsedBlock', 'expandedBlock');
        Effect.BlindDown(dd, {duration:0.1});
      }
      else {
        shiftClassNames(dl, 'expandedBlock', 'collapsedBlock');
        Effect.BlindUp(dd, {duration:0.1});
      };
      Event.stop(ev);
      return false;
    }
  },
  '#app #tabslist li' : function(el){
    el.onclick = function(ev){
      if (!el.sel) el.sel = true;
      else {return;};
      var ev = ev?ev:window.event,
          inputs = $A(el.getElementsByTagName('FORM')[0].getElementsByTagName('INPUT')), tmp = [];
      inputs.each(function(e,idx){(0<idx && idx<5)?tmp.push(e.value):''});
      gBeforeEditData[el.id] = tmp;
      Element.addClassName(el, 'editing');
      inputs[1].focus();
      return true;
    };
  },
  '#app #tabslist input.editsave' : function(el){
    el.onclick = function(ev){
      var ev = ev?ev:window.event, v = validateField,
          li = Event.findElement(ev, 'LI'), tds = Event.findElement(ev, 'FORM').getElementsByTagName('INPUT'), title = $F(tds[1]);
      if (v('actname',title) && v('actid',$F(tds[3]))) {
         var dl = li.getElementsByTagName('DL')[1], dd = dl.getElementsByTagName('DD')[0];
         var num = $A($('tabslist').getElementsByTagName('LI')).indexOf(li);
         new Ajax.Request('qpt_edit',
           {parameters:'category='+category+'&num='+num+'&'+Form.serialize(Event.findElement(ev, 'FORM')),
            onSuccess: function(request){
              new Effect.BlindUp(dd, {
                duration : 0.1,
                afterFinish : function(){
                  shiftClassNames(dl, 'expandedBlock', 'collapsedBlock');
                  Element.removeClassName(li, 'editing');
                  li.id = 'tabslist_'+title;
                  var spans = li.getElementsByTagName('SPAN');
                  Element.update(spans[1], title);
                  Element.update(spans[0], $F(tds[2]));
                  Behaviour.apply();
                }
              })
            },
            onFailure: function(request){
              var message = (/Error Value\s*<\/dt>\s*<dd>(.*?)<\/dd>/i).exec(request.responseText);
              window.alert(message[1]);
            },
            onComplete: function(request){if (li.sel) {li.sel = null;};}
           }
         );
      };
      Event.stop(ev);
      return false;
    }
  },
  '#app #tabslist input.editcancel' : function(el){
    el.onclick = function(ev){
      var ev = ev?ev:window.event, li = Event.findElement(ev, 'LI'),
          inputs = $A(li.getElementsByTagName('FORM')[0].getElementsByTagName('INPUT')),
          values = $A(gBeforeEditData[li.id]),
          dl = li.getElementsByTagName('DL')[1], dd = dl.getElementsByTagName('DD')[0];
      values.each(function(el,idx){inputs[idx+1].value = el});
      if (Element.visible(dd)) {
        Effect.BlindUp(dd, {
          duration : 0.1,
          afterFinish : function(){
              shiftClassNames(dl, 'expandedBlock', 'collapsedBlock');
              Element.removeClassName(li, 'editing');
          }
        });
      }
      else {Element.removeClassName(li, 'editing');};
      if (li.sel) {li.sel = null;};
      Event.stop(ev);
      return false;
    }
  },
  '#app #addaction' : function(el){
    el.onsubmit = function(ev){
        document.getElementById('actname').blur();
        return false;
    };
  },
  '#app #actname' : function(el){
    var re = new RegExp('[^a-zA-Z0-9-_~,.\\$\\(\\)# ]','g'), initialVal = $F(el);
    el.onfocus = function(){Element.addClassName('addaction', 'adding');};
    el.onkeyup = function() {
      var name = $F(el), id = $F('actid');
      if (id == initialVal.replace(re,'') || id == name.replace(re,'')) {
        $('actid').value = name.replace(re,'');
        initialVal = name;
      };
    };
  },
  '#app #buttonadd' : function(el){
    el.onclick = function(ev){
      var ev = ev?ev:window.event, v = validateField;
      if (v('actname',$F('actname')) && v('actid',$F('actid'))) {
        var idx = $('tabslist').getElementsByTagName('LI').length;
        new Ajax.Request('qpt_add',
          {parameters:'category='+category+'&idx='+idx+'&'+Form.serialize('addaction'),
           onSuccess: function(request){
             var dl = $('addaction').getElementsByTagName('DL')[3], dd = dl.getElementsByTagName('DD')[0];
             Effect.BlindUp(dd, {
               duration : 0.1,
               afterFinish : function(){
                 shiftClassNames(dl, 'expandedBlock', 'collapsedBlock');
                 new Insertion.Bottom('tabslist', request.responseText);
                 Form.reset('addaction');
                 Element.removeClassName('addaction', 'adding');
                 var dls = $A($('tabslist').getElementsByTagName('DL')).findAll(
                   function(dl){return Element.hasClassName(dl, 'collapseAdvanced');}
                 );
                 collapseLi(dls[dls.length-1]);
                 if ($A($('tabslist').getElementsByTagName('LI').length > 0)) {
                     Element.removeClassName('reorder', 'noitems');
                 };
                 ieHover();
                 Behaviour.apply();
               }
             });
           },
           onFailure: function(request){
             var message = (/Error Value\s*<\/dt>\s*<dd>(.*?)<\/dd>/i).exec(request.responseText);
             window.alert(message[1]);
           }
          }
        );
      };
      return true;
    }
  },
  '#app #buttoncancel' : function(el){
    el.onclick = function(ev){
      var ev = ev ? ev : window.event, dl = $('addaction').getElementsByTagName('DL')[3], dd = dl.getElementsByTagName('DD')[0];
      Effect.BlindUp(dd, {
        duration : 0.1,
        afterFinish : function(){
          shiftClassNames(dl, 'expandedBlock', 'collapsedBlock');
          Form.reset('addaction');
          Element.removeClassName('addaction', 'adding');
          Behaviour.apply();
       }
      });
      Event.stop(ev);
      return false;
    }
  },
  '#app #generated_tabs' : function(el){
    el.onclick = function(ev){
      new Ajax.Request('qpt_setproperty', {
        parameters : 'generated_tabs='+el.checked,
        onSuccess : function(){
          new Ajax.Updater({success:'roottabs'}, 'qpt_getroottabs', {
            method : 'get',
            onComplete : function(){
              el.attachEvent?ieHover():'';
              Behaviour.apply();
            }
          });
       }
      });
    }
  }
};

/* Registerin previous rules with Behaviour.js */

Behaviour.register(myrules);

/* Registering global handlers for Ajax requests through Prototype */

var globalHandlers = {
  onCreate: function(){Element.addClassName('app', 'working');},
  onComplete: function() {if(Ajax.activeRequestCount == 0) Element.removeClassName('app', 'working');}
};

Ajax.Responders.register(globalHandlers);

/* Adding event listeners for hovering in IE & collapsing Advanced sections on loading */

Event.observe(window, 'load', collapseAdvanced);
Event.observe(window, 'load', function() {
    var category_input = document.getElementById('actions_category');
    if (category_input && typeof(category_input.value) != 'undefined') {
        category_input.value ? category = category_input.value : {};
    };
});
Event.observe(window, 'unload', function(){gBeforeReorderFragment = null; gBeforeEditData = null;});

if (window.attachEvent) {Event.observe(window, 'load', ieHover, false);}

/* Utility functions */

function ieHover(){
  $A($('app').getElementsByTagName('LI')).each(function(el){
    if (el.attachEvent){
      if (!el.hovers) el.hovers = {};
      if (el.hovers['hover']) return;
      el.hovers['hover'] = true;
      el.attachEvent('onmouseover', function(){
        if (!Element.hasClassName(el, 'onHover')) {Element.addClassName(el, 'onHover');};
      });
      el.attachEvent('onmouseout',  function(){Element.removeClassName(el, 'onHover');});
    }
  });
};

function collapseLi(dl) {
  var dd = dl.getElementsByTagName('DD')[0];
  if (!Element.hasClassName(dl, 'collapsedBlock') && Element.visible(dd)) {
    shiftClassNames(dl, 'expandedBlock', 'collapsedBlock');
  };
  Element.hide(dd);
};

function collapseAdvanced() {
  var dls = $A($('app').getElementsByTagName('DL')).findAll(
    function(dl){return Element.hasClassName(dl, 'collapseAdvanced');}
  );
  $A(dls).each(collapseLi);
};

function shiftClassNames(el, from, to) {
  Element.removeClassName(el, from);
  Element.addClassName(el, to);
};

function validateField(id, val) {
  var re = new RegExp('[^a-zA-Z0-9-_~,.\$\(\)# ]','g');
  if (!val) {
    window.alert(id.replace(/act/,'') + ' field is required!');
    document.getElementById(id).focus();
    return false;
  }
  else {
    er = id != 'actid' ? true : val.search(re) == -1 ? true : false;
    if (!er) {
      window.alert(val+' is not a legal name.\n The following characters are invalid:' + val.match(re).toString());
      document.getElementById(id).focus();
    }
  }
  return er;
};

function removeEdition(el) {
  var el = el?el:'tabslist';
  $A($(el).getElementsByTagName('LI')).each(function(li,idx){if(li != el) li.onclick='';});
};