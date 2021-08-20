module.exports = function (RED) {
    function searchHash(config) {
        const utils = require('../utils/utils')

        var node = this
        this.server = RED.nodes.getNode(config.server)
        node.topic = 'search hash'

        node.file = __dirname + '/searchHash.py'

        node.config = {
            input: config.input,
            output: config.output,
            root: this.server.url,
            apikey: this.server.apikey,
            hash: config.hash
        }

        utils.run(RED, node, config)
    }
    RED.nodes.registerType("search hash", searchHash);
}

