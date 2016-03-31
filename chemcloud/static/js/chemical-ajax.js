$(document).ready(function(){

	$('.changeorder').click(function(){
		var stepid   = $(this).attr("data-stepid");
		var direct   = $(this).attr("data-direction");
		var me       = $(this);
		var reac_id  = $(this).attr("data-reacid");
		var schem_id = $(this).attr("data-schemeid");
		var url = '/chemical/reaction/'+reac_id+'/scheme/'+ schem_id +'/change_order/'; 
		var id_name = 'btn_'+stepid+direct;

		$.getJSON(url, {step_id: stepid, direction: direct}, function(data){
	/*$(this) после get уже не живет. Надо заново определять элемент по селектору. При этом, похоже, надо определять по id, а не по классу. Иначе возвращаются все элементы класса. Хотя можно вычислить номер элемента по порядку стадии и направлению*/

	/*варианты вывода в консоль инфы:
	console.log('tut');. текст
	console.log($('.changeorder')) тэг элемента что ли
	console.dir(pel); вся инфа об элементе
	*/
		var pel = $('#'+id_name);
		var pel = pel.parent('td');
		var tdorder_cur = pel.next();
		pel = pel.parent('tr');
		var tdorder_neighbor;

		var arr   = JSON.parse(data);
		var cur_order = arr.cur_step_order;
		var neighbor_order = arr.neighbor_step_order;
		var cur_id = arr.cur_step_id;
		var neighbor_id = arr.neighbor_step_id;

		if (direct == 'up')
		{	
	/*	 	tdorder_neighbor = pel.prev().children().eq(1) порядок у нас во втором столбце, но чтобы не завязываться на порядок, найдем столбец с порядком по id
	*/
			tdorder_neighbor = pel.prev().children('#order_'+neighbor_id)
			tdorder_cur.html(cur_order);
			tdorder_neighbor.html(neighbor_order);
			pel.insertBefore(pel.prev());
		}
		else
		{
			tdorder_neighbor = pel.next().children('#order_'+neighbor_id)
			tdorder_cur.html(cur_order);
			tdorder_neighbor.html(neighbor_order);
			pel.insertAfter(pel.next());	
		}
		return false;
	 });
	});

});
