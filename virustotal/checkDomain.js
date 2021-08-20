module.exports = function (RED) {
    function checkDomain(config) {
        const utils = require('../utils/utils')

        var node = this
        this.server = RED.nodes.getNode(config.server)
        node.topic = 'check domain'

        node.file = __dirname + '/checkDomain.py'

        node.config = {
            apikey: this.server.apikey,
            domain: config.domain
        }

        utils.run(RED, node, config)
    }
    RED.nodes.registerType("check domain", checkDomain);
}

