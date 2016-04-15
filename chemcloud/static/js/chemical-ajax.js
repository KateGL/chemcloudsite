// using jQuery
//эта вещь нужна, чтобы можно было передавать POST запросы
function getCookie(name) { 
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function(){
//=====================================================================
//=== УНИВЕРСАЛЬНЫЙ ОБРАБОТЧИК РЕДАКТИРОВАНИЯ ЯЧЕЕК ТАБЛИЦ ============
//Присваиваем таблице уникальный идентификатор id, который соответствует названию таблицы и через нижнее подчеркивание нужные и реакции, эксперимента и т.д. .
//Редактируемым ячейкам (td) присваиваем класс — edit, класс с названием столбца в БД и числовой класс с идентификатором строки в БД (ид стадии, или ид точки эксперимента, и т.д.).
//=====================================================================
	//при нажатии на ячейку таблицы с классом edit
	$('td.edit').click(function(){
		//находим input внутри элемента с классом ajax и вставляем вместо input его значение
		$('.ajax').html($('.ajax input').val());
		//удаляем все классы ajax
		$('.ajax').removeClass('ajax');
		//Нажатой ячейке присваиваем класс ajax
		$(this).addClass('ajax');
		//внутри ячейки создаём input и вставляем текст из ячейки в него
		$(this).html('<input id="editbox" size="'+ $(this).text().length+'" type="text" value="' + $(this).text() + '" />');
		//устанавливаем фокус на созданном элементе
		$('#editbox').focus();
		});

	//определяем нажатие кнопки на клавиатуре
	$('td.edit').keydown(function(event){
		//получаем значение класса и разбиваем на массив
		//в итоге получаем такой массив - arr[0] = edit, arr[1] = наименование столбца, arr[2] = id строки
		//проверяем какая была нажата клавиша и если была нажата клавиша Enter (код 13)
		if(event.which == 13)
		{
			arr = $(this).attr('class').split( " " );
			//получаем наименование таблицы, в которую будем вносить изменения
			var table_str = $('table').attr('id');
			//выполняем ajax запрос методом POST
			//в файл update_cell.php
			//создаём строку для отправки запроса
			//value = введенное значение
			//id = номер строки
			//field = название столбца
			//table = название таблицы - в названии таблицы поместить через _ нужные ид
			var url_str  = "/chemical/cell_update/";
			var csrftoken = getCookie('csrftoken');//эта вещь нужна, чтобы можно было передавать POST запросы
			var data_str = "value="+$('.ajax input').val()+"&id="+arr[2]+"&field="+arr[1]+"&table="+table_str+"&csrfmiddlewaretoken="+csrftoken;
			 $.ajax({ type: "POST", url: url_str, data: data_str,
				//при удачном выполнении скрипта, производим действия
				 success: function(data){
					//находим input внутри элемента с классом ajax и вставляем вместо input его значение
					 $('.ajax').html($('.ajax input').val());
					//удаялем класс ajax
					 $('.ajax').removeClass('ajax');

			 }});
	 	}
	});

	//убираем input при нажатии вне поля ввода, если не хотим сохранять введенную информацию
	$(document).on('blur', '#editbox', function(){
			td_el = $(this).parent();			
			arr = td_el.attr('class').split( " " );
			var table_str = $('table').attr('id');
			var url_str  = "/chemical/cell_value/";
			var csrftoken = getCookie('csrftoken');
 		 $.post(url_str, {id: arr[2], field: arr[1], table: table_str, csrfmiddlewaretoken:  csrftoken},function(data){
					var arr   = JSON.parse(data);
					old_val = arr.value;
					//находим input внутри элемента с классом ajax и вставляем вместо input его значение
					 $('.ajax').html(old_val);
					//удаялем класс ajax
					 $('.ajax').removeClass('ajax');

			 }, 'JSON');
	});

//=====================================================================
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
			tr_str = tr_str + '<td><button id="btn_' + id_step + 'up" data-stepid="' + id_step + '" data-direction="up"  type="button" data-reacid="'+reac_id+'" data-schemeid="'+schem_id+'">&#9650</button></br><button id="btn_' + id_step + 'down" class="changeorder" data-stepid="' + id_step + '" data-direction="down"  type="button"  data-reacid="'+reac_id+'" data-schemeid="'+schem_id+'">&#9660</button></td>';

			tr_str = tr_str + '<td id="order_' + id_step + '"> '+step_order+' </td>';
			tr_str = tr_str + '<td>'+step_name+'</td>';
			tr_str = tr_str + '<td></td>';//сама стадия пока пустая
			tr_str = tr_str + '<td><a href="{% url \'step_detail\' ' + reac_id + ' ' + schem_id + ' ' + id_step + '"> Детали</a> </td>';
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
			var btn_cur = $('#'+id_name);
			var pel = btn_cur.parent('td');
			pel = pel.parent('tr');
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
