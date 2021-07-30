module.exports = function (RED) {
    function checkFile(config) {
        const utils = require('../utils/utils')

        var node = this
        this.server = RED.nodes.getNode(config.server)
        node.topic = 'check file'

        node.file = __dirname + '/checkFile.py'

        node.config = {
            apikey: this.server.apikey,
            hash: config.hash
        }

        utils.run(RED, node, config)
    }
    RED.nodes.registerType("check file", checkFile);
}

