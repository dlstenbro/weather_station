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
  success: function(data){
   // Perform operation on return value
   console.log(data);
  },
  complete:function(data){
   setTimeout(fetchdata,5000);
  }
 });
}

$(document).ready(function(){
 setTimeout(fetchdata,5000);
});
