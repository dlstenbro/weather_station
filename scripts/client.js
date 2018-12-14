// support modern web browsers
if(window.XMLHttpRequest){

	xmlhttp = new XMLHttpRequest();

} else{
	// supports older web browsers
	xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");

}


var data_element = document.getElementById("data").innerHTML;
console.log(data_element);

document.getElementById("data").innerHTML = "update data";

//xmlhttp.open("GET", "/scripts/test.txt", true);
//xmlhttp.send();
