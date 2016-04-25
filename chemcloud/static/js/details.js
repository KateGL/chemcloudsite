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
    return ebox.val();
    }

function set_readbox_value(rbox, value){
    if (rbox.attr('type') == 'checkbox'){

        if(value == 'True'){
            rbox.prop('checked', true);}//attr("checked","checked");}
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
        clone.attr('id','editbox');
        if(rbox.hasClass('form-control')){
            //alert(rbox.val());
            clone.val(rbox.val());}
        return clone;
    }

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


function after_save_value(json_msg, btn_save, val_td, edt_td, ebox, evalue){
        //call refresh method
        //alert('call refresh');
        if(btn_save.attr("refresh_page") == "True")
        {location.reload(); return false;}
        //alert('after call refresh');
       // try {
         //     var target = $(this).attr("after_save");
         //     if(typeof target != 'undefined'){
         //     window[target]();}
         //   }catch(e){alert(target);}

        //hide input
        set_readbox_value(val_td.children(":first"),evalue);
        //alert('after call set_readbox_value');
        ebox.removeAttr('id');
        edt_td.html('');
        edt_td.hide();
        val_td.show();
        //alert('after hide');
        btn_save.addClass('disabled');
        btn_save.siblings(".detail_btn_edit").removeClass('disabled');

        return false;
    }




$(document).ready(function(){
    $('.detail_caption').addClass('text-right');
    $('.detail_edit').hide().addClass('text-left').css({ 'font-weight': "bold" });
    $('.detail_value').addClass('text-left').css({ 'font-weight': "bold" });
    $('.detail_btn_edit').addClass('btn btn-lg btn-link').html('<span class="glyphicon glyphicon-edit"></span>');
    $('.detail_btn_save').addClass('btn btn-lg btn-link disabled').html('<span class="glyphicon glyphicon-ok"></span>');


    $('#detail_main').on("click", "button.detail_btn_edit", function(){
        var parnt = $(this).parent('td');
        var edt_td = parnt.siblings(".detail_edit");
        var val_td = parnt.siblings(".detail_value");
        var clone = clone_rbox(val_td.children(":first"));
        edt_td.append(clone);
        edt_td.show();
        val_td.hide();

        clone.focus();
        $(this).addClass('disabled');
        $(this).siblings(".detail_btn_save").removeClass('disabled');


        return false;
        }
    );

    $('#detail_main').on("click", "button.detail_btn_save", function(){
        //send ajax json
        var url_str  = $('#detail_main').attr('url_edit');
        var csrftoken = getCookie('csrftoken');//эта вещь нужна, чтобы можно было передавать POST запросы

        //alert(url_str);
        //alert(csrftoken);
        var parnt = $(this).parent('td');
        var edt_td = parnt.siblings(".detail_edit");
        var val_td = parnt.siblings(".detail_value");
        var ebox = $('#editbox');
        var evalue = get_editbox_value(ebox);
        var btn_save = $(this);
        var fldname = parnt.attr('field_name');
        //alert(evalue);
        //alert(fldname);
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
            btns.children('.detail_btn_save').addClass('disabled');
            btns.children('.detail_btn_edit').removeClass('disabled');

            return false;
        }, 500);

        }
    );


});


