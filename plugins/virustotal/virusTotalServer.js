module.exports = function (RED) {
    function VirusTotalServerNode(n) {
        RED.nodes.createNode(this, n);
        this.apikey = n.apikey;
    }
    RED.nodes.registerType("virus-total-server", VirusTotalServerNode);
}
