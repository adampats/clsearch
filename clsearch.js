// search craigslist
console.log('Loading function...');

exports.handler = function(event, context) {
  console.log('functionName: ', context.functionName);
  console.log('AWSrequestID: ', context.awsRequestId);
  console.log('remaining time: ', context.getRemainingTimeInMillis());
  console.log('logGroupName: ', context.logGroupName);
  console.log('logStreamName: ', context.logStreamName);

  console.log("GET URL: " + event.url);

  var http = require('http');
  http.get(event.url, function (res) {
    console.log("Response statusCode: " + res.statusCode);
    console.log("Response headers:");
    console.log(res.headers);
    res.resume();
  }).on('error', function (e) {
    console.error("Got error: " + e.message);
  });
  context.succeed("success lulz");
};
