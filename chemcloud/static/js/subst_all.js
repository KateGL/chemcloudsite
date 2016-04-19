function redirect_to_search(str){
    window.location.href = '/chemical/substance/search/'+str;
    return false;
    }

$(document).ready(function(){
   $("#search").keyup(function(){
      var str = $(this).val()
      if (str==''){
          $("#txtHint").html('');}
      else {
      var url = "/chem_ajax/substance/search_hint/"+ str;
      $("#txtHint").load(url);
      }
    });

    $("#search").keypress(function (e){
        var key = e.which;
        if(key == 13)  // the enter key code
        {
         var str = $("#search").val()
         redirect_to_search(str);
        }
    });

    $("#search_btn").click(function(){
        var str = $("#search").val()
        redirect_to_search(str);
        }
    );
});




