#!/usr/bin/env bash

#Variable Declaration
NetAppServer=<SERVER>
AUTH=<AUTH>
NODE_PAYLOAD=''

#Hitting the first endpoint to pull a list of nodes UUIDs & and using jq, clean up json formating of the response
NODE_RAW=$(curl -X GET "https://$NetAppServer/api/cluster/nodes?return_records=true&return_timeout=15" -H "accept: application/json" -H "authorization: $AUTH" -k -s)
NODES=$(echo "$NODE_RAW" | jq '.records[].uuid')

#iterate through the list of UUID from the first call and use them to pull back details on each node.
for NODE in $NODES
do 
    #using SED to strip the quotes from the UUIDs 
    NODE=$(sed -e 's/^"//' -e 's/"$//' <<<"$DISK")
    #hit the API to collect node information for the current UUID
    RESPONSE=$(curl -X GET "https://$NetAppServer/api/cluster/nodes/$NODE?fields=cluster_interfaces,controller,ha,metric,model,name,serial_number,service_processor,state,uptime,uuid,version,vm" -H "accept: application/json" -H "authorization: $AUTH" -k -s)
    #Clean up the JSON Response and merge with previous iterations
    NODE_PAYLOAD=$(echo "$RESPONSE" "$NODE_PAYLOAD" | jq -s '.')
done 

#output the final JSON object with all nodes 
echo $NODE_PAYLOAD | jq '.[].records' | jq '
    [.[] | 
    [leaf_paths as $path | {"key": $path | join("_"), "value": getpath($path)}]
    | from_entries]
  ' | sed "s/[0-9]_//g"|jq '.'
