# node-red-node-asn
[Node-RED](https://nodered.org/) nodes to help users get ASN information when they enter IP address. 
Address needs to be an IPv4 or IPv6 format.

# Example
```
The node expects input and output from msg.payload by default,
but if you want to specify another path you can specify it in the Input/Output field.

Input:
'2001:43f8:7b0::'
Output:
{'asn': '37578',
 'asn_cidr': '2001:43f8:7b0::/48',
 'asn_country_code': 'KE',
 'asn_date': '2013-03-22',
 'asn_description': 'Tespok, KE',
 'asn_registry': 'afrinic'}
 ```

# Installation
```
npm i node-red-node-asn
```

# Website
https://www.dtonomy.com/
