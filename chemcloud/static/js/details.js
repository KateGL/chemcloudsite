function get_editbox_value(ebox){
    if (ebox.attr('type') == 'checkbox'){
        if( ebox.is(':checked')){return "True";}else{return "False";}
        }
    return ebox.val();
    }

function set_readbox_value(rbox, value){
    if (rbox.attr('type') == 'checkbox'){

        if(value == 'True'){
            rbox.attr("checked","checked");}
        else{
            rbox.removeAttr("checked");}
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


$(document).ready(function(){
    $('.detail_caption').addClass('text-right');
    $('.detail_edit').hide().addClass('text-left').css({ 'font-weight': "bold" });
    $('.detail_value').addClass('text-left').css({ 'font-weight': "bold" });
    $('.detail_btn_edit').addClass('btn btn-md btn-link').html('<span class="glyphicon glyphicon-edit"></span>');
    $('.detail_btn_save').addClass('btn btn-md btn-link disabled').html('<span class="glyphicon glyphicon-ok"></span>');


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

        //process errors

        //call refresh method
        if($(this).attr("refresh_page")== "True")
        {location.reload(); return false;}
       // try {
         //     var target = $(this).attr("after_save");
         //     if(typeof target != 'undefined'){
         //     window[target]();}
         //   }catch(e){alert(target);}

        //hide input

        var parnt = $(this).parent('td');
        var edt_td = parnt.siblings(".detail_edit");
        var val_td = parnt.siblings(".detail_value");
        var ebox = $('#editbox');
        var evalue = get_editbox_value(ebox);
        //alert(evalue);
        set_readbox_value(val_td.children(":first"),evalue);

        ebox.removeAttr('id');
        edt_td.html('');
        edt_td.hide();
        val_td.show();

        $(this).addClass('disabled');
        $(this).siblings(".detail_btn_edit").removeClass('disabled');
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


