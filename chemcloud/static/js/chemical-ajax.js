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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

//=====================================================================
//=== УНИВЕРСАЛЬНЫЙ ОБРАБОТЧИК РЕДАКТИРОВАНИЯ ЯЧЕЕК ТАБЛИЦ ============
//Присваиваем таблице уникальный идентификатор id, который соответствует названию таблицы и через нижнее подчеркивание нужные и реакции, эксперимента и т.д. .
//Редактируемым ячейкам (td) присваиваем класс — edit, класс с названием столбца в БД и числовой класс с идентификатором строки в БД (ид стадии, или ид точки эксперимента, и т.д.).
//=====================================================================

	//$('button.editbtn').click(function(){ 
   $('tbody').on("click", "button.editbtn", function(){
      console.log('button.editbtn');
		ptd = $(this).parent('div');
        ptd = ptd .parent('td');
        arr = ptd.attr('class').split( " " );
        var id  = arr[1]+arr[2];
		$('.ajax'+id).html($('.ajax'+id+' input').val());
		//удаляем все классы ajax
		//$('.ajax'+id).removeClass('ajax');
		ptd.addClass('ajax'+id);
		//внутри ячейки создаём input и вставляем текст из ячейки в него
		ptd.html('<span hidden>'+ptd.text()+' </span> <input id="editbox'+id+'" size="'+ ptd.text().length+'" type="text" value="' + ptd.text() + '" /> <div class="div-right"><button type="button" class="save"  ><span class="glyphicon glyphicon-floppy-disk"></span></button> <button type="button" class="revert"  ><span class="glyphicon glyphicon-remove"></span></button></div');
		//устанавливаем фокус на созданном элементе
		$('#editbox'+id).focus();
		});

   $('tbody').on("click", "button.save", function(){
		//получаем значение класса и разбиваем на массив
		//в итоге получаем такой массив - arr[0] = edit, arr[1] = наименование столбца, arr[2] = id строки
		ptd = $(this).parent('div');
        ptd = ptd .parent('td');
		arr = ptd.attr('class').split( " " );
        arr = ptd.attr('class').split( " " );
        var id  = arr[1]+arr[2];
		//получаем наименование таблицы, в которую будем вносить изменения
		var table_str = $('table').attr('id');
        var evalue = $('.ajax'+id + ' input').val();

		//выполняем ajax запрос методом POST
		//в файл update_cell.php
		//создаём строку для отправки запроса
		//value = введенное значение
		//id = номер строки
		//field = название столбца
		//table = название таблицы - в названии таблицы поместить через _ нужные ид
		var url_str  = $('table').attr("data-url-cellupdate");
		var csrftoken = getCookie('csrftoken');//эта вещь нужна, чтобы можно было передавать POST запросы
        var data_to_edit = {
            value: evalue,
            id: arr[2],
            field: arr[1],
            table: table_str
        }

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });


		 $.ajax({ type: "POST", url: url_str, 
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data_to_edit),
            dataType: 'json',
			//при удачном выполнении скрипта, производим действия
			 success: function(data){
				var arr   = JSON.parse(data);
				var result = arr.result;			
				var errorText = arr.errorText;
                var messageText = arr.messageText;
                var messageText = arr.messageText;
                var tr_class = arr.tr_class;
                console.log(tr_class)
				if (result == 'success')		
				{//находим input внутри элемента с классом ajax и вставляем вместо input его значение
				 	$('.ajax'+id).html($('.ajax'+id+' input').val() + '<div class="div-right"><button type="button" class="editbtn"  ><span class="glyphicon glyphicon-pencil"></span></button></div>');
					//удаялем класс ajax
                    var ptr = $('.ajax'+id).parent('tr');
                    old_class = ptr.attr('class');
				 	$('.ajax'+id).removeClass('ajax'+id);
                    if (messageText.length !=0)
                        alert(messageText);
                    if (tr_class.length !=0)
                        ptr.addClass(tr_class);
                    else
                        ptr.removeClass(old_class);
               
				}
				else
				{
					alert(errorText);
					var el = $('#editbox');
	            el.blur();

				}	
			},								
			 error: function(jqXHR, textStatus, errorThrown) { 
		        alert(jqXHR.statusText);

				}
		 });
		});

   $('tbody').on("click", "button.revert", function(){
      console.log('tut_delete');
		ptd = $(this).parent('div');
    	td_el = ptd.parent('td');				
		arr = td_el.attr('class').split( " " );
        var id  = arr[1]+arr[2];
		var csrftoken = getCookie('csrftoken');
        var old_val = $('.ajax'+id+' span').text();
        $('.ajax'+id).html(old_val + '<div class="div-right"><button type="button" class="editbtn"  ><span class="glyphicon glyphicon-pencil"></span></button></div>');
		//удаялем класс ajax
		 $('.ajax'+id).removeClass('ajax'+id);
		});

	//при нажатии на ячейку таблицы с классом edit	
	//$('td.edit').click(function(){ Катя! у тебя поля фикированные, не добавляемые, ты так вызывай метод
/*   $(document).on('click', 'td.edit', function(){
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
		});*.

	//определяем нажатие кнопки на клавиатуре
//	$('td.edit').keydown(function(event){ Катя! у тебя поля фикированные, не добавляемые, ты так вызывай метод

	$(document).on('keydown', 'td.edit', function(event){
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
					var arr   = JSON.parse(data);
					var result = arr.result;			
					var errorText = arr.errorText;
					if (result == 'success')		
					{//находим input внутри элемента с классом ajax и вставляем вместо input его значение
					 	$('.ajax').html($('.ajax input').val());
						//удаялем класс ajax
					 	$('.ajax').removeClass('ajax');
					}
					else
					{
						alert(errorText);
						var el = $('#editbox');
		            el.blur();

					}	
				},								
				 error: function(jqXHR, textStatus, errorThrown) { 
			        alert(jqXHR.statusText);

					}
			 });
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
console.log('old_val='+old_val);	

			 }, 'JSON');
	});
*/
//====================================================================

