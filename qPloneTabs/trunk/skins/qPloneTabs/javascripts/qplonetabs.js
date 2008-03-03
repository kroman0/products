/* Global variables */

var gBeforeReorderData = [];        // storage for actions before sorting
var gBeforeReorderFragment = null;  // document fragment for insertion in UL after clicking cancel button after reorder
var gBeforeEditData = {};           // hash for storage tabs fields before editing
var category = 'portal_tabs';

/* Main part - rules for element on our form */

var myrules = {
  '#app #reorder' : function(el){
    el.onclick = function(ev){
      var ev = ev ? ev : window.event;
      // remember current actions state for 'cancel sorting' case
//       gBeforeReorderFragment = document.getElementById('tabslist').innerHTML;
      var lis = $A($('tabslist').getElementsByTagName('LI'));
      gBeforeReorderData = [];
      lis.each(function(el, idx) {
          gBeforeReorderData.push(grepInfo(el));
      });

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
               inpt.type == 'hidden' ? inpt.value = idx : inpt.name = inpt.name.replace(/i\d+_/, 'i'+idx+'_');
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
      var ev = ev ? ev : window.event;
      Sortable.destroy('tabslist');
      shiftClassNames('app', 'sorting', 'viewing');

      // update action to before sorting state
//      Element.update('tabslist', gBeforeReorderFragment);
      var tabslist = $('tabslist');
      tabslist.innerHTML = "";
      for (var i = 0, li; li = gBeforeReorderData[i]; i++) {
          tabslist.appendChild(recoverAction(li));
      }

      el.attachEvent ? ieHover() : '';
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
Event.observe(window, 'unload', function() {
    // cleanup memory to prevent memory lack
    delete gBeforeReorderFragment;
    delete gBeforeEditData;
    delete gBeforeReorderData
});

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
  var el = el ? el : 'tabslist';
  $A($(el).getElementsByTagName('LI')).each(function(li,idx){if(li != el) li.onclick=function(event){return false;};});
};


//**********************************************

//    Fixed bug: innerHTML return not actual data, now used DOM


function grepInfo(li) {
    
    // grep li state
    var info = {"li.id" : li.id, "li.title": li.title, "li.className" : li.className};
    
    // grep visibility checkbox state
    var vis_box = li.getElementsByTagName("INPUT")[0];
    info["vis_box.checked"] = vis_box.checked;
    info["vis_box.name"] = vis_box.name;
    
    var spans = li.getElementsByTagName("SPAN");
    
    // grep url helper state
    info["url_helper.text"] = spans[0].innerHTML;
    
    // grep tab title state
    info["tab_title.text"] = spans[1].innerHTML;
    
    // grep edit form state
    var edit_form = li.getElementsByTagName("FORM")[0];
    info["edit_form.name"] = edit_form.name;
    info["edit_form.action"] = edit_form.action;
    
    var inputs = edit_form.getElementsByTagName("INPUT");
    
    // grep hidden input index value
    info["input_idx.value"] = inputs[0].value;
    
    // grep action name input state
    info["input_name.name"] = inputs[1].name;
    info["input_name.value"] = inputs[1].value;
    
    // grep dl advanced section class name
    info["dl_advanced.className"] = edit_form.getElementsByTagName("DL")[1].className;
    info["dd_advanced.style.display"] = edit_form.getElementsByTagName("DD")[1].style.display;
    
    // grep url input state
    info["input_url.name"] = inputs[2].name;
    info["input_url.value"] = inputs[2].value;
    
    // grep id input state
    info["input_id.name"] = inputs[3].name;
    info["input_id.value"] = inputs[3].value;
    
    // grep condition input state
    info["input_condition.name"] = inputs[4].name;
    info["input_condition.value"] = inputs[4].value;
    
    // grep buttons state
    info["save_button.value"] = inputs[5].value;
    info["cancel_button.value"] = inputs[6].value;
    
    return info;
}

function recoverAction(info) {
    
    // create list item and assign corresponding attributes
    var li = document.createElement("LI");
    li.id = info["li.id"];
    li.title = info["li.title"];
    li.className = info["li.className"];
    
    // create drag handle image and assign corresponding attributes
    var drag_handle = document.createElement("IMG");
    drag_handle.className = "drag-handle";
    drag_handle.src = "drag.gif";
    drag_handle.alt = "";
    drag_handle.height = "11";
    drag_handle.width = "25";
    
    li.appendChild(drag_handle);
    
    // create bridge div element for visibility checkbox
    var bridge = document.createElement("DIV");
    bridge.className = "bridge";
    
    // create checkbox for visibility control
    var vis_box = document.createElement("INPUT");
    vis_box.type = "checkbox";
    vis_box.className = "visibility";
    vis_box.value = "1";
    vis_box.title = "visibility";
    vis_box.name = info["vis_box.name"];
    
    bridge.appendChild(vis_box);

    // buggy IE
    if (info["vis_box.checked"]) {
        vis_box.setAttribute("checked", "checked");
        vis_box.defaultChecked = true;
    }

    li.appendChild(bridge);
    
    // create Delete link
    var del_link = document.createElement("A");
    del_link.className = "delete";
    del_link.href = "#";
    del_link.appendChild(document.createTextNode("Delete"));
    
    li.appendChild(del_link);
    
    // create url-helper element
    var url_helper = document.createElement("SPAN");
    url_helper.className = "url-helper";
    url_helper.appendChild(document.createTextNode(info["url_helper.text"]));
    
    li.appendChild(url_helper);
    
    // create tab title element
    var tab_title = document.createElement("SPAN");
    tab_title.className = "tab-title";
    tab_title.appendChild(document.createTextNode(info["tab_title.text"]));
    
    li.appendChild(tab_title);
    
    // create edit form
    var edit_form = document.createElement("FORM");
    edit_form.className = "editform";
    edit_form.method = "post";
    edit_form.name = info["edit_form.name"];
    edit_form.action = info["edit_form.action"];
    
    // create hidden input with index value
    var input_idx = document.createElement("INPUT");
    input_idx.type = "hidden";
    input_idx.name = "idx";
    input_idx.value = info["input_idx.value"];
    
    edit_form.appendChild(input_idx);
    
    // create dl element for name input section
    var dl_name = document.createElement("DL");
    var dt_name = document.createElement("DT");
    var name_label = document.createElement("LABEL");
    name_label.appendChild(document.createTextNode("Name"));
    
    dt_name.appendChild(name_label);
    dl_name.appendChild(dt_name);
    
    // crete input for action name
    var dd_name = document.createElement("DD");
    var input_name = document.createElement("INPUT");
    input_name.type = "text";
    input_name.size = "30";
    input_name.name = info["input_name.name"];
    input_name.value = info["input_name.value"];
    
    dd_name.appendChild(input_name);
    dl_name.appendChild(dd_name);
    edit_form.appendChild(dl_name);
    
    // create dl element for advanced inputs
    var dl_advanced = document.createElement("DL");
    dl_advanced.className = info["dl_advanced.className"];
    
    // create collapsible header
    var dt_advanced = document.createElement("DT");
    dt_advanced.className = "headerAdvanced";
    dt_advanced.appendChild(document.createTextNode("Advanced"));
    
    dl_advanced.appendChild(dt_advanced);
    
    // create collapsible content
    var dd_advanced = document.createElement("DD");
    dd_advanced.className = "contentAdvanced";
    dd_advanced.style.display = info["dd_advanced.style.display"];
    
    // add URL section
    // add url header
    var dl_url = document.createElement("DL");
    var dt_url = document.createElement("DT");
    var label_url = document.createElement("LABEL");
    label_url.appendChild(document.createTextNode("URL (Expression)"));
    
    dt_url.appendChild(label_url);
    dl_url.appendChild(dt_url);
    
    //add url value
    var dd_url = document.createElement("DD");
    var input_url = document.createElement("INPUT");
    input_url.type = "text";
    input_url.size = "30";
    input_url.name = info["input_url.name"];
    input_url.value = info["input_url.value"];
    
    dd_url.appendChild(input_url);
    dl_url.appendChild(dd_url);
    dd_advanced.appendChild(dl_url);
    
    // add ID section
    // add id header
    var dl_id = document.createElement("DL");
    var dt_id = document.createElement("DT");
    var label_id = document.createElement("LABEL");
    label_id.appendChild(document.createTextNode("Id"));
    
    dt_id.appendChild(label_id);
    dl_id.appendChild(dt_id);
    
    //add id value
    var dd_id = document.createElement("DD");
    var input_id = document.createElement("INPUT");
    input_id.type = "text";
    input_id.name = info["input_id.name"];
    input_id.value = info["input_id.value"];
    
    dd_id.appendChild(input_id);
    dl_id.appendChild(dd_id);
    dd_advanced.appendChild(dl_id);
    
    // add Condition section
    // add condition header
    var dl_condition = document.createElement("DL");
    var dt_condition = document.createElement("DT");
    var label_condition = document.createElement("LABEL");
    label_condition.appendChild(document.createTextNode("Condition (Expression)"));
    
    dt_condition.appendChild(label_condition);
    dl_condition.appendChild(dt_condition);
    
    //add condition value
    var dd_condition = document.createElement("DD");
    var input_condition = document.createElement("INPUT");
    input_condition.type = "text";
    input_condition.size = "30";
    input_condition.name = info["input_condition.name"];
    input_condition.value = info["input_condition.value"];
    
    dd_condition.appendChild(input_condition);
    dl_condition.appendChild(dd_condition);
    dd_advanced.appendChild(dl_condition);
    
    // add visual clear div to advanced dd element
    var visual_clear = document.createElement("DIV");
    visual_clear.className = "visualClear";
    visual_clear.appendChild = document.createTextNode("<!-- -->");
    
    dd_advanced.appendChild(visual_clear);
    dl_advanced.appendChild(dd_advanced);
    edit_form.appendChild(dl_advanced);
    
    // create div element for form controls
    var form_controls = document.createElement("DIV");
    
    // add save button
    var save_button = document.createElement("INPUT");
    save_button.type = "submit";
    save_button.className = "editsave";
    save_button.value = info["save_button.value"];
    form_controls.appendChild(save_button);
    
    // add cancel button
    var cancel_button = document.createElement("INPUT");
    cancel_button.type = "submit";
    cancel_button.className = "editcancel";
    cancel_button.value = info["cancel_button.value"];
    form_controls.appendChild(cancel_button);
    
    edit_form.appendChild(form_controls);
    li.appendChild(edit_form);

    return li;
}