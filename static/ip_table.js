$(document).ready(function(){
   $(".dnstoggle").click(function(){
      $(".dnsname").toggle();
   });
   $(":checkbox").change(function(){
      var subnet = $(this).attr('value');
      $("#"+subnet).toggle();
   });
});
