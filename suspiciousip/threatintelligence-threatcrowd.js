/**
 * Copyright JS Foundation and other contributors, http://js.foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 **/

module.exports = function (RED) {
    "use strict";
    const https = require("https");
    var hashSum = require("hash-sum");

    function threatcrowd(n) {
        RED.nodes.createNode(this, n);
        var node = this;

        this.on("input", function (msg) {
            // get ip and then out 
            var url = "https://www.threatcrowd.org/searchApi/v2/ip/report/?ip=" + msg.payload.ip;

            // some of the logic is copied from httprequest node
            var req = https.get(url, function (res) {
                // Force NodeJs to return a Buffer (instead of a string)
                // See https://github.com/nodejs/node/issues/6038
                res.setEncoding(null);
                delete res._readableState.decoder;

                msg.statusCode = res.statusCode;
                msg.responseUrl = res.responseUrl;
                msg.payload = [];

                res.on('data', function (chunk) {
                    if (!Buffer.isBuffer(chunk)) {
                        // if the 'setEncoding(null)' fix above stops working in
                        // a new Node.js release, throw a noisy error so we know
                        // about it.
                        throw new Error("HTTP Request data chunk not a Buffer");
                    }
                    msg.payload.push(chunk);
                });
                res.on('end', function () {

                    // Check that msg.payload is an array - if the req error
                    // handler has been called, it will have been set to a string
                    // and the error already handled - so no further action should
                    // be taken. #1344
                    if (Array.isArray(msg.payload)) {
                        // Convert the payload to the required return type
                        msg.payload = Buffer.concat(msg.payload); // bin

                        var jsonResponse = JSON.parse(msg.payload.toString('utf8'));
                        // chunked encoding can not coexist with content length in header    
                        // https://stackoverflow.com/questions/3304126/chunked-encoding-and-content-length-header
                        msg.headers = {};
                        msg.headers["Content-Type"] = "application/json";
                        msg.headers["Access-Control-Allow-Origin"] = "*";
                        msg.headers["Access-Control-Allow-Headers"] = "X-Requested-With";

                        msg.payload = {
                            "votes": jsonResponse.votes,
                            "permalink": jsonResponse.permalink ? jsonResponse.permalink : "https://www.threatcrowd.org/ip.php?ip=" + msg.payload.ip, 
                            "source": "www.threatcrowd.org",
                            "votesPretty": jsonResponse.votes < 0 ? "Malicious" : "Benign"
                        };

                        node.send(msg);
                        node.status({});
                    }
                });
            });

            req.on('error', function (err) {
                node.error(err, msg);
                msg.payload = err.toString() + " : " + url;
                msg.statusCode = err.code;
                node.send(msg);
                node.status({ fill: "red", shape: "ring", text: err.code });
            });
        });
    }
    RED.nodes.registerType("ti-threatcrowd", threatcrowd);
}
