module.exports = function (RED) {
    function checkUrl(config) {
        const utils = require('../utils/utils')

        var node = this
        this.server = RED.nodes.getNode(config.server)
        node.topic = 'check url'

        node.file = __dirname + '/checkUrl.py'

        node.config = {
            apikey: this.server.apikey,
            url: config.url
        }

        utils.run(RED, node, config)
    }
    RED.nodes.registerType("check url", checkUrl);
}

