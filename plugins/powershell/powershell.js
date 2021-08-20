const shell = require('node-powershell');



module.exports = function(RED) {
    function PowershellNode(config) {
        RED.nodes.createNode(this, config);
        this.func = config.func;
        this.username = config.username;
        this.password = config.password;
        let ps = new shell({
            executionPolicy: 'Bypass',
            noProfile: true
        });

        this.on('input', function(msg) {
            msg.func = this.func;
            msg.username = this.username;
            msg.password = this.password; 
            if (msg.func) {
                var res = msg.func.replace(/%username%/g, msg.username);
                res = res.replace(/%password%/g, msg.password);
                ps.addCommand(res);
            } else if (typeof msg.payload == 'string') {
                var res = msg.payload.replace(/%username%/g, msg.username);
                res = res.replace(/%password%/g, msg.password);
                ps.addCommand(res);
            } else {
                var sh = "Write-Host Please Provide a Script"
                ps.addCommand(sh);
            }
            ps.invoke()
            .then(output => {
                msg.payload = output;
                this.send([output, null]);
            })
            .catch(error => {
                msg.payload = error;
                this.error(error);
            });
        });

        this.on('close', function() {

            ps.dispose();
        })
    }



    RED.nodes.registerType("powershell", PowershellNode);
}