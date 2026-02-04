#!/usr/bin/env bash
#Variable Declaration
NetAppServer=<SERVER>
AUTH=<AUTH>


#Hitting the first endpoint to pull a list of Cluster UUIDs & and using jq, clean up json formating of the response
curl -X GET "https://$NetAppServer/api/cluster?return_records=true&return_timeout=15" -H "accept: application/json" -H "authorization: $AUTH" -k -s | jq '.' | jq '
    [. | 
    [leaf_paths as $path | {"key": $path | join("_"), "value": getpath($path)}]
    | from_entries]
  '| sed "s/[0-9]_//g"|jq '.'