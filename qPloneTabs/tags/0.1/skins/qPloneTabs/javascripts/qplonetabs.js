var myrules = {
  '#reorder' : function(el){
    el.onclick = function(){
      Element.classNames('app').set('sorting');
      Sortable.create('tabslist', {handle: 'drag-handle'});
      removeEdition(el);
      return false;
    }
  },
  '#save' : function(el){
    el.onclick = function(){
      var params = '';
      $A($('tabslist').getElementsByTagName('INPUT')).findAll(function(h){return h.type=='hidden';}).each(function(f,idx){params += idx==0?'idxs='+f.value:'&idxs='+f.value;});
      new Ajax.Request('qpt_reorder',
        {method: 'post',
         parameters: params,
         onSuccess: function(request){
           $A($('tabslist').getElementsByTagName('INPUT')).findAll(function(h){return h.type=='hidden';}).each(function(f,idx){f.value=idx;});
           Element.classNames('app').set('viewing');
           Sortable.destroy('tabslist');
           new Effect.Highlight('tabslist',{});
         },
         onComplete: function(request){
           $A($('tabslist').getElementsByTagName('LI')).each(function(li){new Element.ClassNames(li).remove('hover');});
           Behaviour.apply();
         }
        }
      );
      return false;
    }
  },
  '#cancel' : function(el){
    el.onclick = function(){
      new Ajax.Request('qpt_gettabslist',
        {method: 'get',
         onSuccess: function(request){Element.update('tabslist',request.responseText.replace(/collapsedOnLoad/g,'collapsedBlockCollapsible'));},
         onComplete: function(request){Element.classNames('app').set('viewing');Behaviour.apply();}
        }
      );
      Sortable.destroy('tabslist');
      return false;
    }
  },
  'app #tabslist li' : function(el){
     if (el.attachEvent){
      if (!el.hovers) el.hovers = {};
      if (el.hovers['hover']) return;
      el.hovers['hover'] = true;
      el.attachEvent('onmouseover', function(){el.className += ' hover';});
      el.attachEvent('onmouseout',  function(){el.className = el.className.replace((new RegExp('\\s+hover')),'');});
     }
  },
  '.delete' : function(el){
    el.onclick = function(ev){
      var item = el.parentNode,
          num = $A($('tabslist').getElementsByTagName('LI')).indexOf(item);
      new Ajax.Request('qpt_delete',
        {parameters:'idx='+num+'&id=' + item.id.replace('tabslist_', ''),
         onComplete: function(request) {
           new Effect.Fade(item, {duration: 0.7, afterFinish: function(){Element.remove(item);}});
             }
        }
      );
      return false;
    }
  },
  'app #tabslist dt.collapsibleHeader' : function(el){el.onclick = toggleCollapsible;},
  '#tabslist li span' : function(el){
    el.onclick = function(){
      var li = el.parentNode;
      Element.classNames('app').set('editing');
      removeEdition(el);
      Element.classNames(li).set('current');
    }
  },
  '#tabslist input.editsave' : function(el){
    el.onclick = function(ev){
      var ev = ev?ev:window.event, v = validateField,
          li = Event.findElement(ev, 'LI'), tds = document.getElementsByTagName('INPUT');
      if (v('actname',$F(tds[1])) && v('actid',$F(tds[3]))) {
         var num = $A($('tabslist').getElementsByTagName('LI')).indexOf(li);
         new Ajax.Request('qpt_edit',
           {parameters:'num='+num+'&'+Form.serialize(Event.findElement(ev, 'FORM')),
            onSuccess: function(request){
              Element.update(li, request.responseText);
              Element.classNames('app').set('viewing');
              Element.classNames(li).set('');
              li.id = 'tabslist_'+$F(tds[3]);
           },
           onFailure: function(request){
             var message = (/Error Value\s*<\/dt>\s*<dd>(.*?)<\/dd>/i).exec(request.responseText);
             window.alert(message[1]);
           },
           onComplete: function(){Behaviour.apply();}
          }
        );
      };
      return false;
    }
  },
  '#tabslist input.editcancel' : function(el){
    el.onclick = function(ev){Behaviour.apply();
      var ev = ev?ev:window.event;
      new Ajax.Request('qpt_gettabslist',
        {method: 'get',
         onSuccess: function(request){
           Element.update('tabslist',request.responseText.replace(/collapsedOnLoad/g,'collapsedBlockCollapsible'));
           Element.classNames('app').set('viewing');
           Element.classNames(Event.findElement(ev, 'LI')).set('');
         },
         onComplete: function(request){Behaviour.apply();}
        }
      );
      return false;
    }
  },
  '#actname' : function(el){
    var re = new RegExp('[^a-zA-Z0-9-_~,.\$\(\)# ]','g'), initialVal = $F(el);
    el.onfocus = function(){
      Element.classNames('app').set('adding');
      removeEdition(el);
    };
    el.onkeyup = function() {
      var name = $F(el), id = $F('actid');
      if (id == initialVal.replace(re,'') || id == name.replace(re,'')) {
        $('actid').value = name.replace(re,'');
        initialVal = name;
      };
    };
  },
  '#buttonadd' : function(el){
    el.onclick = function(){
      var v = validateField;
      if (v('actname',$F('actname')) && v('actid',$F('actid'))) {
        var idx = $('tabslist').getElementsByTagName('LI').length;
        new Ajax.Request('qpt_add',
          {parameters:'idx='+idx+'&'+Form.serialize('addaction'),
           onSuccess: function(request){
             new Insertion.Bottom('tabslist', request.responseText);
             Form.reset('addaction');
             Element.classNames('app').set('viewing');
             Behaviour.apply();
           },
           onFailure: function(request){
             var message = (/Error Value\s*<\/dt>\s*<dd>(.*?)<\/dd>/i).exec(request.responseText);
             window.alert(message[1]);
           }
          }
        );
      };
      return false;
    }
  },
  '#buttoncancel' : function(el){
    el.onclick = function(){
      Element.classNames('app').set('viewing');
      Form.reset('addaction');
      Behaviour.apply();
      return false;
    }
  },
  '#generated_tabs' : function(el){
    el.onclick = function(ev){new Ajax.Request('qpt_setproperty', {parameters:'generated_tabs='+el.checked});}
  }
};

Behaviour.register(myrules);

var globalHandlers = {
  onCreate: function(){Element.addClassName('app', 'working');},
  onComplete: function() {if(Ajax.activeRequestCount == 0) Element.removeClassName('app', 'working');}
};

Ajax.Responders.register(globalHandlers);

function validateField(id, val) {
  var re = new RegExp('[^a-zA-Z0-9-_~,.\$\(\)# ]','g');
  if (!val) {
    window.alert(id.replace(/act/,'') + ' field is required!');
    return false;
  }
  else {
    er = id != 'actid' ? true : val.search(re) == -1 ? true : false;
    if (!er) window.alert(val+' is not a legal name.\n The following characters are invalid:' + val.match(re).toString());
  }
  return er;
};

function removeEdition(el) {
  $A($('tabslist').getElementsByTagName('SPAN')).each(function(sp,idx){if(sp != el) sp.onclick='';});
};