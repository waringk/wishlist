const express = require('express');

let app = express();
app.set('port', 4758);

const https = require('https')


app.get('/phrases', function(req, res, next) {
  callDatamuse(req.query.mode, req.query.input).then((result) => {
    res.json(result);
  })
});

app.get('/words', function(req, res, next) {
  let mode = req.query.mode;
  let words = req.query.input.replace(/[^\w\s]/gi, '').split(' ');

  let promises = []
  for (const element of words) {
    promises.push(callDatamuse(mode, element));
  }
  
  Promise.all(promises).then((result) => {
    res.json([].concat.apply([], result))
  });
});

app.use(function(req,res){
    res.type('text/plain');
    res.status(404);
    res.send('404 - No Page Here!');
});
  
app.use(function(err, req, res, next){
  console.error(err.stack);
  res.type('plain/text');
  res.status(500);
  res.send('500 - Server Error');
});

app.listen(app.get('port'), function(){
  console.log(`Express started on http://localhost:${app.get('port')}; press Ctrl-C to terminate.`);
});

function callDatamuse(mode, input) {
  return new Promise((resolve, reject) => {
    https.get(`https://api.datamuse.com/words?${mode}=${input}`, (resp) => {
      let data = '';
  
      resp.on('data', (chunk) => {
        data += chunk;
      });
  
      resp.on('end', () => {
        resolve(JSON.parse(data));
      });
    })
    .on("error", (err) => {
      console.log("Error: " + err.message);
    });
  });
}