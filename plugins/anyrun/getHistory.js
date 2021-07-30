module.exports = function (RED) {
    function getHistory(config) {
        const utils = require('../utils/utils')
        var node = this
        this.server = RED.nodes.getNode(config.server)
        node.topic = 'get history'
        node.file = __dirname + '/getHistory.py'
        node.config = {
            username: this.server.username,
            password: this.server.skey,
            skip: config.skip,
        }
        utils.run(RED, node, config)
    }
    RED.nodes.registerType("get history", getHistory);

}