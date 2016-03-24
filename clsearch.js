// search craigslist
console.log('Loading function...');

var http = require('http');

exports.httpHandler = function(url, context) {
  console.log("GET URL: " + url);
  http.get(url, function (res) {
    console.log("Response statusCode: " + res.statusCode);
    console.log("Response headers:");
    console.log(res.headers);
    res.resume();
    context.succeed();
  }).on('error', function (e) {
    console.error("Got error: " + e.message);
    context.done(null, "error");
  });
};

// main
exports.handler = function(event, context) {
  console.log('functionName: ', context.functionName);
  console.log('AWSrequestID: ', context.awsRequestId);
  console.log('remaining time: ', context.getRemainingTimeInMillis());
  console.log('logGroupName: ', context.logGroupName);
  console.log('logStreamName: ', context.logStreamName);

  exports.httpHandler(event.url, context);
};
