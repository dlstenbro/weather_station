var today = new Date();
var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
var dateTime = date+' '+time;

var tempf = 0;
var humidity = 0 ;
var baromin = 0;

var charttype = 'line';
var chart;

var data = {
  labels: [ "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" ],
  datasets: [{
    label: "Temperature",
    fill: true,
    lineTension: 0.1,
    backgroundColor: "rgba(0,255,0,0.4)",
    borderColor: "green", // The main line color
    borderCapStyle: 'square',
    pointBorderColor: "white",
    pointBackgroundColor: "green",
    pointBorderWidth: 1,
    pointHoverRadius: 8,
    pointHoverBackgroundColor: "yellow",
    pointHoverBorderColor: "green",
    pointHoverBorderWidth: 2,
    pointRadius: 4,
    pointHitRadius: 10,
    spanGaps: true,
    data: [0, 0, 0, 0, 0, 0, 0]
  },{label: "Humidity",
    fill: true,
    lineTension: 0.1,
    backgroundColor: "rgba(255,0,0,0.4)",
    borderColor: "green", // The main line color
    borderCapStyle: 'square',
    pointBorderColor: "white",
    pointBackgroundColor: "green",
    pointBorderWidth: 1,
    pointHoverRadius: 8,
    pointHoverBackgroundColor: "yellow",
    pointHoverBorderColor: "green",
    pointHoverBorderWidth: 2,
    pointRadius: 4,
    pointHitRadius: 10,
    spanGaps: true,
    data: [0, 0, 0, 0, 0, 0, 0]}, 
             
    {label: "Barometric Pressure",
    fill: true,
    lineTension: 0.1,
    backgroundColor: "rgba(0,0,255,0.4)",
    borderColor: "green", // The main line color
    borderCapStyle: 'square',
    pointBorderColor: "white",
    pointBackgroundColor: "green",
    pointBorderWidth: 1,
    pointHoverRadius: 8,
    pointHoverBackgroundColor: "yellow",
    pointHoverBorderColor: "green",
    pointHoverBorderWidth: 2,
    pointRadius: 4,
    pointHitRadius: 10,
    spanGaps: true,
    data: [0, 0, 0, 0, 0, 0, 0]}
            ]
};

var timeout = 5000; // 5 seconds

function randint(max, min){
  return JSON.stringify(Math.floor(Math.random() * (max - min) + min));
}

// ajax call to fetch data every 5 seconds from server
function fetchdata(){
  $.ajax({
  //url: '/update_client',
  type: 'get',
  success: function(jsonData){
   // Perform operation on return value
   //console.log(jsonData);

   tempf = randint(100, 40);
   humidity = randint(120, 60);
   baromin = randint(200, 90);
   var data = "tempf: " + tempf + " humidity: " + humidity + " baromin: " + baromin
   document.getElementById("sensor_data").innerHTML = data;
   displayChart();
  },
  complete:function(jsonData){
   setTimeout(fetchdata,timeout);
  }
  });
}

$(document).ready(function(){
  initChart();
 setTimeout(fetchdata,timeout);
});

function initChart(){
  var ctx = document.getElementById('myChart').getContext('2d');
  chart = new Chart(ctx, {
    type: charttype,
    data: data
  });
}

function displayChart(){
  //console.log(chart.data.datasets[0].data);
  //console.log(today.getDay());
  var day = today.getDay();
  
  chart.data.datasets[0].data[day] = tempf;
  chart.data.datasets[1].data[day] = humidity;
  chart.data.datasets[2].data[day] = baromin;
  chart.update();
}

function removeData(chart) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}