


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