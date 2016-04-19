$(document).ready(function(){
	$('#add_step').click(function(){
		/*
		способы вставить строку:
		1) $('<tr id="new_id_id"><td>more content ' + n + '</td><td>more content</td></tr>').insertAfter($('tr:last'));
		2) $('#all-steps').append('<tr/>');
		$('#all-steps tr:last').append('<td/>');
		$('#all-steps tr:last td:first').val('<p>Im a td!</p>');
		или $('#all-steps tr:last td:first').text('<p>Im a td!</p>');

		var n = $('#all-steps tr').length; //текущее число строк, включая строку заголовков. Для определения порядка новой стадии по умолчанию
		*/

		var reac_id  = $(this).attr("data-reacid");
		var schem_id = $(this).attr("data-schemeid");

		var url = '/chemical/reaction/'+reac_id+'/scheme/'+ schem_id +'/step/new/';
		$.getJSON(url, {}, function(data){

			var arr   = JSON.parse(data);
			var step_order = arr.order;
			var step_name = arr.name;
			var id_step = arr.id_step;
			var tr_str = '<tr class="even">';
			tr_str = tr_str + '<td><button id="btn_' + id_step + 'up" class="changeorder" data-stepid="' + id_step + '" data-direction="up"  type="button" data-reacid="'+reac_id+'" data-schemeid="'+schem_id+'">&#9650</button></br><button id="btn_' + id_step + 'down" class="changeorder" data-stepid="' + id_step + '" data-direction="down"  type="button"  data-reacid="'+reac_id+'" data-schemeid="'+schem_id+'">&#9660</button></td>';

			tr_str = tr_str + '<td id="order_' + id_step + '"> '+step_order+' </td>';
			tr_str = tr_str + '<td class="edit name '+id_step + '">'+step_name+'</td>';
			tr_str = tr_str + '<td class="edit step '+id_step + '"></td>';//сама стадия пока пустая
			tr_str = tr_str + '<td><button id="btn_' + id_step + 'del" class="step_delete" type="button" class="btn btn-default"  data-reacid="' + reac_id + '" data-schemeid="' + schem_id + '" data-stepid="' + id_step + '" data-toggle="tooltip" data-placement="top" title="Удалить стадию"><span class="glyphicon glyphicon-remove"></span></button> </td>';
			tr_str = tr_str + '<td><a href="/chemical/reaction/'+reac_id+'/scheme/'+ schem_id +'/step/'+id_step + '/detail/"> Детали</a> </td>';
			tr_str = tr_str + '</tr>';
			$(tr_str).insertAfter($('tr:last'));
			return true;	
		});
	});

	$('#steps_body').on("click", "button", function(){
		if (!$(this).hasClass('step_delete')) //чтобы не реагировало на кнопки изменения порядка
			return false;
		var stepid   = $(this).attr("data-stepid");
		var reac_id  = $(this).attr("data-reacid");
		var schem_id = $(this).attr("data-schemeid");
		var id_name = 'btn_'+stepid+'del';		
		var url = '/chemical/reaction/'+reac_id+'/scheme/'+ schem_id +'/step_delete/';

		$.getJSON(url, {step_id: stepid}, function(data){
			var arr   = JSON.parse(data);
			var cur_order = arr.deleted_step_order;
			var btn_cur = $('#'+id_name);
			var pel = btn_cur.parent('td');
			pel = pel.parent('tr');
         //этот элемент удалим, а последующим понизим порядок. Раз сюда зашли, значит во вью порядок успешно всем последующим стадиям понизился 
		  var b=true;
        pel_next = pel.next('tr');
        var new_order = parseInt(cur_order, 10);
        while (pel_next.length==1)
        { 
          tdorder = pel_next.children().eq(1); //завязались на последовательность столбцов
			 tdorder.text(new_order);
          new_order = new_order+1;
 		    pel_next = pel_next.next('tr');
		   }
			pel.remove();
		});
	});

	//$('.changeorder').click(function(){
	$('#steps_body').on("click", "button", function(){//делегированная обработка события, так как обработчик к новым добавляемым строкам не прикрепляется, а дублировать код обработчика через метод bind не хочется
if (!$(this).hasClass('changeorder')) //чтобы не реагировало на кнопку удаления стадии
			return false;	
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

		var arr   = JSON.parse(data);
		var cur_order = arr.cur_step_order;
		var neighbor_order = arr.neighbor_step_order;
		var cur_id = arr.cur_step_id;
		var neighbor_id = arr.neighbor_step_id;
		var steps_count = arr.steps_count;

		if (cur_id == -1 || neighbor_id == -1 || cur_order == -1 ||neighbor_order == -1)
			return false;

		var btn_cur = $('#'+id_name);
		var pel = btn_cur.parent('td');
		var tdorder_cur = pel.next();
		pel = pel.parent('tr');
		var tdorder_neighbor;

		if (direct == 'up')
		{	
			/*	 	tdorder_neighbor = pel.prev().children().eq(1) порядок у нас во втором столбце, но чтобы не завязываться на порядок, найдем столбец с порядком по id
			*/
			tdorder_neighbor = pel.prev().children('#order_'+neighbor_id)
			//выставляем новый порядок в столбце с порядком			
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

		//крайние кнопки засерим
/*		var btn_first = $('#'+id_name);
		if (cur_order == 1 || cur_order == steps_count)
			btn_cur.attr('class', 'btn-default');
		else
			btn_cur.attr('class', 'changeorder');


		if (neighbor_order == 1 || neighbor_order == steps_count)
			btn_cur.attr('class', 'btn-default');
		else
			btn_cur.attr('class', 'changeorder');
*/
		return false;
	 });
	});

});
