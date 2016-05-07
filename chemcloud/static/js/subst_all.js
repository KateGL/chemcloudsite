function redirect_to_search(){
    var srch = $("#search");
    var str = srch.val();
    if(str.trim()){
     var url = srch.attr('data-search-url').replace('___',str)
     window.location.href = url;
     }
    return false;
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
});




