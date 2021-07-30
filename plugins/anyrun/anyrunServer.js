module.exports = function (RED) {
    function anyrunServer(n) {
        RED.nodes.createNode(this, n);
        this.username = n.username;
        this.password = n.password;
    }
    RED.nodes.registerType("anyrun server", anyrunServer);
}