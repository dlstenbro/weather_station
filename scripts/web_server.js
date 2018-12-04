var http = require('http');
var fs = require('fs');
var port = "8080"

var server = http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/html'});
    console.log('request was made: ' + req);
    var myReadStream = fs.createReadStream("index.html", 'utf8');
    myReadStream.pipe(res);
})

server.listen(port);
console.log("Server started! Listening on port " + port );
