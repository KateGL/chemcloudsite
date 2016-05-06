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

String.prototype.toUTF8 = function() {
    var n, s = '';
    for (var i = 0, iTextLen = this.length; i < iTextLen; i++) {
        n = this.charCodeAt(i);
        if (n < 128) s += String.fromCharCode(n);
        else if (n < 2048) s += String.fromCharCode(192 | n >> 6) + String.fromCharCode(128 | n & 63);
        else if (n < 65536) s += String.fromCharCode(224 | n >> 12) + String.fromCharCode(128 | n >> 6 & 63) + String.fromCharCode(128 | n & 63);
        else s += String.fromCharCode(240 | n >> 18) + String.fromCharCode(128 | n >> 12 & 63) + String.fromCharCode(128 | n >> 6 & 63) + String.fromCharCode(128 | n & 63);
    };
    return s;
};
String.prototype.UrlEncode = function() {
    return this.toUTF8().replace( /[^-_\.!~*'\(\)\da-zA-Z]/g , function(ch) {
        var c = ch.charCodeAt(0).toString(16);
        if (c.length == 1) c = '0' + c;
        return '%' + c;
    });
};

//=====================================================================
//=== УНИВЕРСАЛЬНЫЙ ОБРАБОТЧИК РЕДАКТИРОВАНИЯ ЯЧЕЕК ТАБЛИЦ ============
//Присваиваем таблице уникальный идентификатор id, который соответствует названию таблицы и через нижнее подчеркивание нужные и реакции, эксперимента и т.д. .
//Редактируемым ячейкам (td) присваиваем класс — edit, класс с названием столбца в БД и числовой класс с идентификатором строки в БД (ид стадии, или ид точки эксперимента, и т.д.).
//=====================================================================

	//$('button.editbtn').click(function(){ 
   $('tbody').on("click", "button.editbtn", function(){
      console.log('tut');
		ptd = $(this).parent('td');
		$('.ajax').html($('.ajax input').val());
		//удаляем все классы ajax
		$('.ajax').removeClass('ajax');
		ptd.addClass('ajax');
console.log(ptd);
		//внутри ячейки создаём input и вставляем текст из ячейки в него
		ptd.html('<input id="editbox" size="'+ ptd.text().length+'" type="text" value="' + ptd.text() + '" /> <button type="button" class="save step 123"  ><span class="glyphicon glyphicon-floppy-disk"></span></button> <button type="button" class="delete step 123"  ><span class="glyphicon glyphicon-remove"></span></button>');
		//устанавливаем фокус на созданном элементе
		$('#editbox').focus();
		});

   $('tbody').on("click", "button.save", function(){
      console.log('tut_save');
		//получаем значение класса и разбиваем на массив
		//в итоге получаем такой массив - arr[0] = edit, arr[1] = наименование столбца, arr[2] = id строки
		ptd = $(this).parent('td');
		arr = ptd.attr('class').split( " " );
		//получаем наименование таблицы, в которую будем вносить изменения
		var table_str = $('table').attr('id');
        var value = $('.ajax input').val();
        value = value.toUTF8().UrlEncode();//кодируем передаваемое значение, иначе символ + не передается
		//выполняем ajax запрос методом POST
		//в файл update_cell.php
		//создаём строку для отправки запроса
		//value = введенное значение
		//id = номер строки
		//field = название столбца
		//table = название таблицы - в названии таблицы поместить через _ нужные ид
		var url_str  = "/chemical/cell_update/";
		var csrftoken = getCookie('csrftoken');//эта вещь нужна, чтобы можно было передавать POST запросы
		var data_str = "value="+value+"&id="+arr[2]+"&field="+arr[1]+"&table="+table_str+"&csrfmiddlewaretoken="+csrftoken;
		 $.ajax({ type: "POST", url: url_str, data: data_str,
			//при удачном выполнении скрипта, производим действия
			 success: function(data){
				var arr   = JSON.parse(data);
				var result = arr.result;			
				var errorText = arr.errorText;
                var messageText = arr.messageText;
				if (result == 'success')		
				{//находим input внутри элемента с классом ajax и вставляем вместо input его значение
				 	$('.ajax').html($('.ajax input').val() + '<button type="button" class="editbtn"  ><span class="glyphicon glyphicon-pencil"></span></button>');
					//удаялем класс ajax
				 	$('.ajax').removeClass('ajax');
                    if (messageText.length !=0)
                        alert(messageText);
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

   $('tbody').on("click", "button.delete", function(){
      console.log('tut_delete');
			td_el = $(this).parent('td');				
			arr = td_el.attr('class').split( " " );
console.log(arr);
			var table_str = $('table').attr('id');
			var url_str  = "/chemical/cell_value/";
			var csrftoken = getCookie('csrftoken');
 		 $.post(url_str, {id: arr[2], field: arr[1], table: table_str, csrfmiddlewaretoken:  csrftoken},function(data){
					var arr   = JSON.parse(data);
					old_val = arr.value;
					//находим input внутри элемента с классом ajax и вставляем вместо input его значение
					 $('.ajax').html(old_val + '<button type="button" class="editbtn"  ><span class="glyphicon glyphicon-pencil"></span></button>');
					//удаялем класс ajax
					 $('.ajax').removeClass('ajax');
console.log('old_val='+old_val);	

			 }, 'JSON');
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
	/*$(document).on('blur', '#editbox', function(){			
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

//=====================================================================

