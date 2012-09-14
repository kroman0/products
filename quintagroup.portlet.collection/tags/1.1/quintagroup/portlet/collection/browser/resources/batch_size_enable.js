jq(document).ready(function(e){
    var allow = jq('input[id$=allow_batching]')
    var batch_size = jq('input[id$=batch_size]');

    var batch_sizeToggle = function (allow, batch_size) {
      if (allow.is(':checked')) batch_size.removeAttr('disabled');
      else batch_size.attr("disabled", 'true');
    };

    batch_sizeToggle(allow, batch_size);
    allow.change(function () {
      batch_sizeToggle(allow, batch_size);
    });});
