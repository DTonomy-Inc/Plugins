module.exports = function (RED) {
    function scanFile(config) {
        const utils = require('../utils/utils')

        var node = this
        this.server = RED.nodes.getNode(config.server)
        node.topic = 'scan file'

        node.file = __dirname + '/scanFile.py'

        node.config = {
            input: config.input,
            output: config.output,
            root: this.server.url,
            apikey: this.server.apikey,
            deep_scan: config.deep_scan,
            simplified_output: config.simplified_output
        }

        utils.run(RED, node, config)
    }
    RED.nodes.registerType("scan file", scanFile);
}

