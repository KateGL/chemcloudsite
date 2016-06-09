

function formatSubstance(subst){

    if(typeof subst.name != 'undefined')
        {
     return subst.name+' ('+subst.formula_brutto_formatted+') '+ subst.detail_link;
     }
    else

     { return '---------'}
    }

function applySelect2(subst_serch_element){
    var url_str = subst_serch_element.attr('data-check-url');



subst_serch_element.select2({

  ajax: {
    url: url_str,
    dataType: 'json',
    delay: 50,
    data: function (params) {
      return {
        q: params.term, // search term
        page: params.page
      };
    },
    processResults: function (data, params) {
       // alert(JSON.stringify(data));
      // parse the results into the format expected by Select2
      // since we are using custom formatting functions we do not need to
      // alter the remote JSON data, except to indicate that infinite
      // scrolling can be used
      params.page = params.page || 1;

      return {
        results: data.items,
        pagination: {
          more: (params.page * 10) < data.total_count
        }
      };
    },
    cache: true
  },
  'language': "ru",
  //tags: "true",
  placeholder: 'first',
  escapeMarkup: function (markup) { return markup; }, // let our custom formatter work
  minimumInputLength: 1,
  allowClear: true,
  templateResult: formatSubstance, // omitted for brevity, see the source of this page
  templateSelection: formatSubstance // omitted for brevity, see the source of this page
});
    }


$(document).ready(function(){

applySelect2($("#id_substance"));

$('#id_substance').on("select2:selecting", function(e) {
   // what you would like to happen
   var bf = e.params.args.data.formula_brutto;
   $('#id_brutto_formula_short').val(bf);
});

$('#id_substance').on("select2:unselect", function(e) {
   // what you would like to happen
   $('#id_brutto_formula_short').val('');
});

});