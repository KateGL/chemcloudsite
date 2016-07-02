
function ChangeVisibleByCheckBox(checkbox, class_name){
    if (checkbox.is(':checked'))
        {$(class_name).show();}
    else
        {$(class_name).hide();}
    }



$(document).ready(function(){
    ChangeVisibleByCheckBox($('#chbox_alias'),'.cptn-alias');
    ChangeVisibleByCheckBox($('#chbox_brutto_short'),'.cptn-brutto_formula_short');


    $('#chbox_alias').click(function() {
      ChangeVisibleByCheckBox($('#chbox_alias'),'.cptn-alias');
    });

    $('#chbox_brutto_short').click(function() {
      ChangeVisibleByCheckBox($('#chbox_brutto_short'),'.cptn-brutto_formula_short');
    });

    process_selector($('.dict_selector'), true);

});