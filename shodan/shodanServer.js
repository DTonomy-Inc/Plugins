module.exports = function (RED) {
    function ShodanServerNode(n) {
        RED.nodes.createNode(this, n);
        this.apikey = n.apikey;
    }
    RED.nodes.registerType("shodan-server", ShodanServerNode);
}
