module.exports = function (RED) {
    function ElasticSearchServerNode(n) {
        RED.nodes.createNode(this, n);
        this.ESEndpoint = n.ESEndpoint;
        this.ESUsername = n.ESUsername;
        this.ESPassword = n.ESPassword;
    }
    RED.nodes.registerType("elastic security-server", ElasticSearchServerNode);
}