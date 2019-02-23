const express = require('express');
const fs = require('fs')
const app = express();
const path = require('path');
const port = 8080;
const root_dir = __dirname + '/..'

const bodyParser = require('body-parser');
const url = require('url');
const querystring = require('querystring');

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.get('/', (request, response) => {
  response.sendFile(path.join(root_dir + '/favicon.ico'));
});

app.get('/index.html', (request, response) => {
  response.sendFile(path.join(root_dir + '/index.html'));
});

app.get('/update', (request, response) => {
  response.sendFile(path.join(root_dir + '/index.html'));
  console.log(request.query);
});

app.listen(port, (err) => {
  if (err) {
    return console.log('port is in use!', err);
  }

  console.log(`server is listening on ${port}`);
});
