//JS for Problem
$(document).ready(function(){


    $('.checkbox_slider_with_collapse').on('change', function() {
    // From the other examples
    //alert('check21!');
    var id_coll = $(this).attr('data_id_collapsed');
    if (this.checked) {
    //alert('check true!');
      //$(this).parents('.panel').first().next().find('.panel-heading a').click();
      //$(this).parents('.panel-collapse').collapse('hide');
      //$('#collapseTwo').collapse('show')
      $(id_coll).collapse('show');
    }
    else
     {
        $(id_coll).collapse('hide');
         }
});
});