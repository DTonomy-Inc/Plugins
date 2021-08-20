module.exports = function (RED) {
    function checkIp(config) {
        const utils = require('../utils/utils')

        var node = this
        this.server = RED.nodes.getNode(config.server)
        node.topic = 'shodan check ip'

        node.file = __dirname + '/checkIp.py'

        node.config = {
            apikey: this.server.apikey,
            ip: config.ip,
            input_path: config.input,
            output_path: config.output
        }

        utils.run(RED, node, config)
    }
    // the registration has to be unique, no conflict
    RED.nodes.registerType("shodan check ip", checkIp);
}

