module.exports = function (RED) {
    function scanUrl(config) {
        const utils = require('../utils/utils')

        var node = this
        this.server = RED.nodes.getNode(config.server)
        node.topic = 'scan url'

        node.file = __dirname + '/scanUrl.py'

        node.config = {
            output : config.output,
            root: this.server.url,
            apikey: this.server.apikey,
            url: config.url,
            deep_scan: config.deep_scan,
            simplified_output: config.simplified_output
        }

        utils.run(RED, node, config)
    }
    RED.nodes.registerType("scan url", scanUrl);
}

