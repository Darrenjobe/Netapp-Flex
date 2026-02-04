#!/usr/bin/env bash

#Variable Declaration
NetAppServer=<SERVER>
AUTH=<AUTH>
DISK_PAYLOAD=''

#Hitting the first endpoint to pull a list of Disk UUIDs & and using jq, clean up json formating of the response
DISK_RAW=$(curl -X GET "https://$NetAppServer/api/storage/disks?return_records=true&return_timeout=15" -H "accept: application/json" -H "authorization: $AUTH" -k -s)
DISKS=$(echo "$DISK_RAW" | jq '.records[].name')

#iterate through the list of UUID from the first call and use them to pull back details on each disk.
for DISK in $DISKS
do
    #using SED to strip the quotes from the UUIDs
    DISK=$(sed -e 's/^"//' -e 's/"$//' <<<"$DISK")
    #hit the API to collect disk information for the current UUID
    RESPONSE=$(curl -X GET "https://$NetAppServer/api/storage/disks/$DISK" -H "accept: application/json" -H "authorization: $AUTH" -k -s)
    #Clean up the JSON Response and merge with previous iterations
    DISK_PAYLOAD=$(echo "$RESPONSE" "$DISK_PAYLOAD" | jq -s '.')
done
#output the final JSON object with all disk and info
echo $DISK_PAYLOAD | jq '.' | jq '
    [.[] |
    [leaf_paths as $path | {"key": $path | join("_"), "value": getpath($path)}]
    | from_entries]
  '| sed "s/[0-9]_//g"|jq '.'
