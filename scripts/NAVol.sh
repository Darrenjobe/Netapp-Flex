#!/usr/bin/env bash
#Variable Declaration
NetAppServer=<SERVER>
VOL_PAYLOAD=''
AUTH=<AUTH>

#Hitting the first endpoint to pull a list of Vol UUIDs & and using jq, clean up json formating of the response
VOLS_RAW=$(curl -X GET "https://$NetAppServer/api/storage/volumes?return_records=true&return_timeout=15" -H "accept: application/json" -H "authorization: $AUTH" -k -s)
VOLS=$(echo "$VOLS_RAW" | jq '.records[].uuid')

#iterate through the list of UUID from the first call and use them to pull back details on each disk.
for VOL in $VOLS
do 
    #using SED to strip the quotes from the UUIDs 
    VOL=$(sed -e 's/^"//' -e 's/"$//' <<<"$VOL")
    #hit the API to collect Volume information for the current UUID
    RESPONSE=$(curl -X GET "https://$NetAppServer/api/storage/volumes/$VOL" -H "accept: application/json" -H "authorization: $AUTH" -k -s)
    #Clean up the JSON Response and merge with previous iterations
    VOL_PAYLOAD=$(echo "$RESPONSE" "$VOL_PAYLOAD" | jq -s '.')
done 
#output the final JSON object with all volumes 
echo $VOL_PAYLOAD | jq '.' | jq '
    [.[] | 
    [leaf_paths as $path | {"key": $path | join("_"), "value": getpath($path)}]
    | from_entries]
  '| sed "s/[0-9]_//g"|jq '.'