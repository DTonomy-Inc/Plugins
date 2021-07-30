module.exports = function (RED) {
    function FalconSandboxServerNode(n) {
        RED.nodes.createNode(this, n);
        if(n.url && n.url !== "") {
            this.url = n.url;
        }
        else {
            this.url = "https://www.hybrid-analysis.com";
        }
        this.apikey = n.apikey;
    }
    RED.nodes.registerType("falcon-sandbox-server", FalconSandboxServerNode);
}
