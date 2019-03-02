// support modern web browsers
if(window.XMLHttpRequest){

  xmlhttp = new XMLHttpRequest();

} else{
  // supports older web browsers
  xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");

}

// ajax call to fetch data every 5 seconds from server
function fetchdata(){
  $.ajax({
  url: '/update_client',
  type: 'get',
  success: function(jsonData){
   // Perform operation on return value
   console.log(jsonData);
   document.getElementById("data").innerHTML = JSON.stringify(jsonData);
  },
  complete:function(jsonData){
   setTimeout(fetchdata,5000);
  }
  });
}

$(document).ready(function(){
 setTimeout(fetchdata,5000);
});
