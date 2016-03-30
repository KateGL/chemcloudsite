$(document).ready(function(){
$('.changeorder').click(function(){
/*	console.log('click');	*/
	var stepid   = $(this).attr("data-stepid");
	var curorder = $(this).attr("data-curorder");
	var direct   = $(this).attr("data-direction");
	var me       = $(this);
	var reac_id  = $(this).attr("data-reacid");
	var schem_id = $(this).attr("data-schemeid");
	var url = '/chemical/reaction/'+reac_id+'/scheme/'+ schem_id +'/change_order/'; 
	$.get(url, {step_id: stepid, cur_order: curorder, direction: direct}, function(data){
               $('#all-steps').html(data);

    });
});

});
