

function formatSubstance(subst){

    if(typeof subst.name != 'undefined')
        {
     return subst.name+' ('+subst.formula_brutto_formatted+') '+ subst.detail_link;
     }
    else

     { return '---------'}
    }



$(document).ready(function(){

var url_str = $(".js-data-example-ajax").attr('data-check-url');

$(".js-data-example-ajax").select2({

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
  //language: "select2/i18n/ru",
  'language': "ru",
  //tags: "true",
  //placeholder: 'first',
  escapeMarkup: function (markup) { return markup; }, // let our custom formatter work
  minimumInputLength: 1,
  templateResult: formatSubstance, // omitted for brevity, see the source of this page
  templateSelection: formatSubstance // omitted for brevity, see the source of this page
});

});