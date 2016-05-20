//Загрузка справочников в элемент select

function populate_dict(md_name, url_str, selector, value_init){
    var model_data = {
            model_name: md_name
        };

    $.ajax(
        {
        type: 'GET',
        async: false,
        url: url_str,
        contentType: 'application/json; charset=utf-8',
        data: model_data,
        dataType: 'json',
        success: function(data){
              //alert(md_name);
              selector.append('<select disabled="disabled" class="box_input"></select>')
              var sel = selector.children().last();

              $.each(data, function(k, v) {
                    sel.append('<option value="'+k+'">'+v+'</option>')
                    }
                  )
              sel.val(value_init);


              //return data;
              },
        error: function(xhr, ajaxOptions, thrownError){alert(JSON.stringify(model_data));}
        }
                );

    }

function load_selections(selector)
{
        var md_name = selector.attr('data-model');
        var url_str = selector.attr('data-url');
        var init_value = selector.attr('data-init-value');
        populate_dict(md_name, url_str, selector,init_value);
        return false;
    }

function process_selector(sel){
    $.each(sel, function(k, value) {
                    load_selections($(value));
                    }
                  )

    }


$(document).ready(function(){
    process_selector($('.dict_selector'));


});