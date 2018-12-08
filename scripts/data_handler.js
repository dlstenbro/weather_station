var spawn = require('child_process').spawn;
var py = spawn('python', ['-u' ,'../app/weather_station.py']);

py.stdout.on('data', function(data){	
	console.log(data.toString('utf8'));
});

py.stderr.on('data', function(data){
  console.log("Error: " + data);
});
