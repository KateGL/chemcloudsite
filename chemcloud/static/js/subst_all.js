$(document).ready(function(){
   $("#search").keyup(function(){ 
      var str = $(this).val()
      var url = "/chemical/substance/search_hint/"+ str;       
      $("#txtHint").load(url);    
    });
});




