function redirect_to_search(){
    var srch = $("#search");
    var str = srch.val();
    if(str.trim()){
     var url = srch.attr('data-search-url').replace('___',str)
     window.location.href = url;
     }
    return false;
    }

    //id="id_formula_brutto"  //Это имя автоматически генерируется формой добавления вещества

function check_isomers(ev){
    var br_formula = $("#id_formula_brutto").val();
    var consist = br_formula;
    var url_str = $("#isomer_url").attr('data-check-url');
    //alert(url_str+' '+url_isomers);

    var data_to_edit = {
            brutto_formula: br_formula,
            top_count: '3'
        };

    $.ajax(
        {
        type: 'GET',
        async: false,
        url: url_str,
        contentType: 'application/json; charset=utf-8',
        data: data_to_edit,
        dataType: 'json',
        success: function(data){
              //alert(JSON.stringify(data));
              alert(data.isomer_count);
              isomer_count = data.isomer_count;
              consist = data.consist_as_string;
              return false;
              },
        error: function(xhr, ajaxOptions, thrownError){alert(JSON.stringify(data_to_edit));}
        }
                );

    //show dialog and ok/cancel submitting
    if(isomer_count != '0')
              {
                  ev.preventDefault();
                  $('#isomer_count').html(isomer_count);
                  var url_isomers = $("#isomer_url").attr('data-isomers-url').replace('___',consist);
                  $('#isomer_list_link').attr('href',url_isomers);
                  $('#ModalCheckIsomer').modal();
                  }

    }


$(document).ready(function(){
   $("#search").keyup(function(){
      var str = $(this).val();
      str.trim();
      if (!str){
          $("#txtHint").html('');}
      else {
      var url = $(this).attr('data-hint-url').replace('___',str)
      $("#txtHint").load(url);
      }
    });

    $("#search").keypress(function (e){
        var key = e.which;
        if(key == 13)  // the enter key code
        {
         redirect_to_search();
        }
    });

    $("#search_btn").click(function(){
        redirect_to_search();
        }
    );


    $('#form_substance').submit(function(e) {
        if ($('#form_substance').attr('data-isomer-ok')=='ok'){return true;}
        else
        {check_isomers(e);}
        }
    );



    $('#btn_isomer_ok').click(function(){
        $('#form_substance').attr('data-isomer-ok','ok');
        $('#form_substance').submit();
        }
    );

    $("[name='save_brutto_btn']").click(function(){
        //check_isomers()
        }
    );
});




