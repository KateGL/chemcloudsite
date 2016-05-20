//эта вещь нужна, чтобы можно было передавать POST запросы
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function get_editbox_value(ebox){
    if (ebox.attr('type') == 'checkbox'){
        if( ebox.is(':checked')){return "True";}else{return "False";}
        }
    //alert(ebox.val());
    return ebox.val();
    }

function set_readbox_value(rbox, value){
    if (rbox.attr('type') == 'checkbox'){

        if(value == 'True'){
            rbox.prop('checked', true);}
        else{
            rbox.prop('checked', false);}
        rbox.val(value);
        return false;
        }
    rbox.val(value);
    return false;
    }

function clone_rbox(rbox){
        clone = rbox.clone();
        clone.removeAttr('disabled');
        clone.addClass('data_edit');
        if(rbox.hasClass('form-control')){
            //alert(rbox.val());
            clone.val(rbox.val());}

        if(rbox.is('select')){
            clone.val(rbox.val());}

        clone.show();
        return clone;
    }

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


function after_save_value(json_msg, btn_save, val_td, edt_td, ebox, evalue){
        //call refresh method
        //alert('call refresh');
        //save_refresh_page
        if(btn_save.parent().attr("save_refresh_page") == "True")
        {location.reload(); return false;}
        //alert('after call refresh');
       // try {
         //     var target = $(this).attr("after_save");
         //     if(typeof target != 'undefined'){
         //     window[target]();}
         //   }catch(e){alert(target);}

        //hide input
        set_readbox_value(val_td.children(":first"),evalue);
        edt_td.html('');
        edt_td.hide();
        val_td.show();

        btn_save.hide();
        btn_save.siblings(".detail_btn_cancel").hide();
        btn_save.siblings(".detail_btn_edit").show();

        return false;
    }




$(document).ready(function(){
    $('.detail_caption').addClass('text-right').addClass('col-md-2');
    $('.detail_btns').addClass('col-md-2')
        .append('<button type="button" class="detail_btn_edit"></button>')
        .append('<button type="button" class="detail_btn_save"></button>')
        .append('<button type="button" class="detail_btn_cancel"></button>');

    $('.detail_edit').hide().addClass('text-left').addClass('col-md-4').css({ 'font-weight': "bold" });
    $('.detail_value').addClass('text-left').addClass('col-md-4').css({ 'font-weight': "bold" });
    $('.box_input').addClass('col-xs-12');
    $('.form-control').addClass('col-xs-12');
    $('.detail_btn_edit').addClass('btn btn-md btn-link').html('<span class="glyphicon glyphicon-edit"></span>');
    $('.detail_btn_save').addClass('btn btn-md btn-link').html('<span class="glyphicon glyphicon-ok"></span>').hide();
    $('.detail_btn_cancel').addClass('btn btn-md btn-link').html('<span class="glyphicon glyphicon-remove"></span>').hide();


    $('#detail_main').on("click", "button.detail_btn_edit", function(){
        var parnt = $(this).parent('td');
        var edt_td = parnt.siblings(".detail_edit");
        var val_td = parnt.siblings(".detail_value");
        var clone = clone_rbox(val_td.children(":first"));
        edt_td.append(clone);
        edt_td.show();
        val_td.hide();

        clone.focus();
        $(this).hide();
        $(this).siblings(".detail_btn_save").show();
        $(this).siblings(".detail_btn_cancel").show();


        return false;
        }
    );


    $('#detail_main').on("click", "button.detail_btn_save", function(){
        //send ajax json
        var url_str  = $('#detail_main').attr('url_edit');
        var csrftoken = getCookie('csrftoken');//эта вещь нужна, чтобы можно было передавать POST запросы

        var parnt = $(this).parent('td');
        var edt_td = parnt.siblings(".detail_edit");
        var val_td = parnt.siblings(".detail_value");
        var ebox = edt_td.find('.data_edit');
        var evalue = get_editbox_value(ebox);
        var btn_save = $(this);
        var fldname = parnt.attr('field_name');
        var data_to_edit = {
            field_name: fldname,
            value: evalue
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

    $('#detail_main').on("click", "button.detail_btn_cancel", function(){
        var parnt = $(this).parent('td');
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

/*remove to snippet!
    $(document.body).on("focusout", '#editbox', function(event){
        var edt_td = $(this).parent('td');
        var val_td = edt_td.siblings(".detail_value");
        var btns = edt_td.siblings('.detail_btns');
        var focused = document.activeElement;
        setTimeout(function(){//timout for waiting send focus to inner elements
            focused = document.activeElement;
            //alert(focused);
            if( $(".detail_btn_save").is( $(focused) )){ return false; }
            edt_td.html('');
            edt_td.hide();
            val_td.show();
            btns.children('.detail_btn_save').hide();//addClass('disabled');
            btns.children('.detail_btn_edit').show();//removeClass('disabled');

            return false;
        }, 500);

        }
    );
*/


});


