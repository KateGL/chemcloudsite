//костыль для второй таблицы экспериментов
//а может и не костыль...

$(document).ready(function(){

    $('#exper_edit_points').on("click", "button.detail_btn_edit", function(){
        //alert('Hi');
        var parnt = $(this).parent();
        var edt_td = parnt.siblings(".detail_edit");
        var val_td = parnt.siblings(".detail_value");
        var clone = append_clone_rbox(val_td.children(":first"), edt_td);

        edt_td.show();
        val_td.hide();

        clone.focus();

        $(this).hide();
        $(this).siblings(".detail_btn_save").show();
        $(this).siblings(".detail_btn_cancel").show();


        return false;
        }
    );


    $('#exper_edit_points').on("click", "button.detail_btn_save", function(){
        //send ajax json
//console.log('trtrtrt');
        var url_str  = $('#exper_edit_points').attr('url_edit');
        var csrftoken = getCookie('csrftoken');//эта вещь нужна, чтобы можно было передавать POST запросы

        var parnt = $(this).parent();
        var edt_td = parnt.siblings(".detail_edit");
        var val_td = parnt.siblings(".detail_value");
        var ebox = edt_td.find('.data_edit');
        var evalue = get_editbox_value(ebox);
        //console.log(evalue);
        var btn_save = $(this);
        var fldname = parnt.attr('field_name');
        var arg_id = parnt.attr('arg_id');
        var subst_id = parnt.attr('subst_id');
        var data_to_edit = {
            field_name: fldname,
            value: evalue,
            argument_id : arg_id,
            substance_id : subst_id
        }
        //alert(JSON.stringify(data_to_edit));
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $.ajax(
        {
        type: 'POST',
        url: url_str,
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data_to_edit),
        dataType: 'json',
        success: function(json_msg){
              //alert(json_msg);
              after_save_value(json_msg, btn_save, val_td, edt_td, ebox, evalue);
              return false;
              },
        error: function(xhr, ajaxOptions, thrownError){alert(JSON.stringify(data_to_edit));}
        }
                );

        return false;
        }
    );

    $('#exper_edit_points').on("click", "button.detail_btn_cancel", function(){
        var parnt = $(this).parent();
        var edt_td = parnt.siblings(".detail_edit");
        var val_td = parnt.siblings(".detail_value");
        var btns = edt_td.siblings('.detail_btns');
        edt_td.show();
        val_td.hide();

        edt_td.html('');
        edt_td.hide();
        val_td.show();
        btns.children('.detail_btn_save').hide();
        btns.children('.detail_btn_cancel').hide();
        btns.children('.detail_btn_edit').show();

        return false;
        }
    );

/*
    $('#exper_edit_points').on("click", "button.argument_delete", function(){
        //send ajax json
//console.log('trtrtrt');

        var url_str  = $('#exper_edit_points').attr('url_edit');
        var csrftoken = getCookie('csrftoken');//эта вещь нужна, чтобы можно было передавать POST запросы

        var parnt = $(this).parent();
        var edt_td = parnt.siblings(".detail_edit");
        var val_td = parnt.siblings(".detail_value");
        var ebox = edt_td.find('.data_edit');
        var evalue = get_editbox_value(ebox);
        //console.log(evalue);
        var btn_save = $(this);
        var fldname = parnt.attr('field_name');
        var arg_id = parnt.attr('arg_id');
        var subst_id = parnt.attr('subst_id');
        var data_to_edit = {
            field_name: fldname,
            value: evalue,
            argument_id : arg_id,
            substance_id : subst_id
        }
        //alert(JSON.stringify(data_to_edit));
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $.ajax(
        {
        type: 'POST',
        url: url_str,
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data_to_edit),
        dataType: 'json',
        success: function(json_msg){
              //alert(json_msg);
              after_save_value(json_msg, btn_save, val_td, edt_td, ebox, evalue);
              return false;
              },
        error: function(xhr, ajaxOptions, thrownError){alert(JSON.stringify(data_to_edit));}
        }
                );


        return false;
        }
    );

*/


});