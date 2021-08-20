module.exports = function (RED) {
    function scanIp(config) {
        const utils = require('../utils/utils')

        var node = this
        this.server = RED.nodes.getNode(config.server)
        node.topic = 'scan ip'

        node.file = __dirname + '/scanIp.py'

        node.config = {
            root: this.server.url,
            apikey: this.server.apikey,
            ip: config.ip,
            deep_scan: config.deep_scan
        }

        utils.run(RED, node, config)
    }
    RED.nodes.registerType("scan ip", scanIp);
}

