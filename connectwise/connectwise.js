const ConnectWiseRest = require('connectwise-rest');


module.exports = function(RED) {
    function ConnectWiseNode(config) {
        const utils = require('../utils/utils')
        RED.nodes.createNode(this, config);
        var node = this
        this.server = RED.nodes.getNode(config.server)
        node.config = {
            companyId: this.server.companyId,
            companyurl: this.server.companyurl,
            publickey: this.server.publickey,
            privatekey: this.server.privatekey,
            clientid: this.server.clientid,
            nameid: config.nameid,
            summary: config.summary,
            description: config.description,
            record: config.record
        }
        const cw = new ConnectWiseRest({
            companyId: this.server.companyId,
            companyUrl:  this.server.companyurl,
            publicKey: this.server.publickey,
            privateKey: this.server.privatekey,
            clientId: this.server.clientid,
            entryPoint: 'v4_6_release', // optional, defaults to 'v4_6_release'
            apiVersion: '3.0.0',        // optional, defaults to '3.0.0'
            timeout: 20000,             // optional, request connection timeout in ms, defaults to 20000
            retry: false,               // optional, defaults to false
            retryOptions: {             // optional, override retry behavior, defaults as shown
            retries: 4,               // maximum number of retries
            minTimeout: 50,           // number of ms to wait between retries
            maxTimeout: 20000,        // maximum number of ms between retries
            randomize: true,          // randomize timeouts
            },
            debug: false,               // optional, enable debug logging
            logger: (level, text, meta) => { } // optional, pass in logging function
        });
        
        this.on('Input', function(msg){
            msg.nameid = config.name;
            msg.company_id = this.server.companyId;
            msg.summary = config.summary;
            msg.description = config.description;
            msg.record = config.record;
            cw.ServiceDeskAPI.Tickets.createTicket({
                summary: msg.summary,
                board: {
                    name: msg.nameid
                },
                company: {
                    identifier: msg.company_id //company ID
                },
                initialDescription: msg.description,
                recordType: msg.record
                //can also pass in any other Ticket object settings as needed
            })
            .then(output => {
                msg.payload = output;
                this.send([output, null]);
            })
            .catch(error => {
                msg.payload = error;
                this.error(error);
            });

        });
    
        utils.run(RED, node, config)
    }
    RED.nodes.registerType("connectwise", ConnectWiseNode);
}