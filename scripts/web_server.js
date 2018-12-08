var http = require('http');
var fs = require('fs');
var port = "8080"

var server = http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/html'});
    console.log('request was made: ' + req.url);

    // weather_station/scripts/web_server.js
    var parent_path = __dirname + "/../"
    if(req.url == "/")
    {
	var myReadStream = fs.createReadStream("index.html", 'utf8');
    }
    else if(req.url == "/favicon.ico")
    {
	var myReadStream = fs.createReadStream("favicon.ico", 'utf8');
    }
    else{
	var myReadStream = fs.createReadStream(parent_path + req.url, 'utf8');
    }
    myReadStream.pipe(res);
})

server.listen(port);
console.log("Server started! Listening on port " + port );


