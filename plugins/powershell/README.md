This node is basically just a node-red wrapper for https://github.com/rannn505/node-powershell/

It does not do much checking yet and is provided as-is.

Input your Powershell script that you want to run as `msg.payload`. The first output of the node is connected to `stdout`, the second one to `stderr` of the shell.