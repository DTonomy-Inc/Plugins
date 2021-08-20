module.exports = function (RED) {
    function checkIp(config) {
        const utils = require('../utils/utils')

        var node = this
        this.server = RED.nodes.getNode(config.server)
        node.topic = 'virus total check ip'

        node.file = __dirname + '/checkIp.py'

        node.config = {
            apikey: this.server.apikey,
            ip: config.ip,
            input: config.input,
            output: config.output,
            simplified_output: config.simplified_output
        }

        utils.run(RED, node, config)
    }
    RED.nodes.registerType("check ip", checkIp);
}

