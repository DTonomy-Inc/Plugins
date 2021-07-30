module.exports = function (RED) {
    function scanUrlToFile(config) {
        const utils = require('../utils/utils')

        var node = this
        this.server = RED.nodes.getNode(config.server)
        node.topic = 'scan url to file'

        node.file = __dirname + '/scanUrlToFile.py'

        node.config = {
            root: this.server.url,
            apikey: this.server.apikey,
            url: config.url
        }

        utils.run(RED, node, config)
    }
    RED.nodes.registerType("scan url to file", scanUrlToFile);
}

