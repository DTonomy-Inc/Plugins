module.exports = function (RED) {
    function connectwiseserver(n) {
        RED.nodes.createNode(this, n);
        this.companyId = n.companyId;
        this.companyurl = n.companyurl;
        this.publickey = n.publickey;
        this.privatekey = n.privatekey;
        this.clientid = n.clientid;
    }
    RED.nodes.registerType("connectwise server", connectwiseserver);
}