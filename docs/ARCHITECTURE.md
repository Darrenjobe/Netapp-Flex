# Architecture

This document explains the architecture and data flow of the NetApp Flex integration.

## Overview

The NetApp Flex integration collects metrics from NetApp ONTAP storage systems via REST API and forwards them to New Relic for monitoring and analysis.

## Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     NetApp ONTAP Cluster                        │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Volumes │  │   Disks  │  │   Nodes  │  │  Cluster │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
│                                                                 │
│              REST API (HTTPS - Port 443)                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ API Calls
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    Linux Server / VM                            │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │         New Relic Infrastructure Agent                  │   │
│  │                                                         │   │
│  │  ┌──────────────────────────────────────────────┐     │   │
│  │  │       New Relic Flex Integration             │     │   │
│  │  │                                               │     │   │
│  │  │  Reads: flex-netapp.yml                      │     │   │
│  │  │  Executes every polling interval (default 30s)│     │   │
│  │  └──────────────┬───────────────────────────────┘     │   │
│  │                 │ Spawns                              │   │
│  │                 │                                     │   │
│  │  ┌──────────────▼───────────────────────────────┐    │   │
│  │  │       Shell Scripts                          │    │   │
│  │  │  • NACluster.sh - Cluster metrics           │    │   │
│  │  │  • NADisk.sh    - Disk inventory            │    │   │
│  │  │  • NANode.sh    - Node health               │    │   │
│  │  │  • NAVol.sh     - Volume metrics            │    │   │
│  │  │                                              │    │   │
│  │  │  Uses: curl, jq, sed, bash                  │    │   │
│  │  └──────────────┬───────────────────────────────┘    │   │
│  │                 │ Returns JSON                       │   │
│  │  ┌──────────────▼───────────────────────────────┐    │   │
│  │  │  Flex parses JSON → New Relic Events        │    │   │
│  │  └──────────────┬───────────────────────────────┘    │   │
│  └─────────────────┼────────────────────────────────────┘   │
│                    │                                         │
└────────────────────┼─────────────────────────────────────────┘
                     │ HTTPS
                     │
┌────────────────────▼─────────────────────────────────────────┐
│                  New Relic Platform                          │
│                                                              │
│  Event Types:                                                │
│  • NetAppVolSample     - Volume metrics                      │
│  • NetAppClusterSample - Cluster information                 │
│  • NetAppDiskSample    - Disk data                           │
│  • NetAppNodeSample    - Node metrics                        │
│                                                              │
│  → Stored in NRDB (New Relic Database)                       │
│  → Queryable via NRQL                                        │
│  → Visualizable in Dashboards                                │
│  → Alertable via Alert Policies                              │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Configuration Loading
- New Relic Infrastructure agent loads `flex-netapp.yml` on startup
- Flex integration parses the configuration to determine which scripts to run

### 2. Script Execution (Every Polling Interval)
For each script (NACluster.sh, NADisk.sh, NANode.sh, NAVol.sh):

1. **Initial API Call**: Retrieve list of resource UUIDs/names
   ```bash
   curl https://<netapp>/api/storage/volumes?return_records=true
   ```

2. **Parse Response**: Extract UUIDs using `jq`
   ```bash
   VOLS=$(echo "$VOLS_RAW" | jq '.records[].uuid')
   ```

3. **Iterate Resources**: Loop through each UUID
   ```bash
   for VOL in $VOLS; do
       RESPONSE=$(curl https://<netapp>/api/storage/volumes/$VOL)
       VOL_PAYLOAD=$(echo "$RESPONSE" "$VOL_PAYLOAD" | jq -s '.')
   done
   ```

4. **Flatten JSON**: Convert nested JSON to flat structure
   ```bash
   jq '[.[] | [leaf_paths as $path | {"key": $path | join("_"), "value": getpath($path)}] | from_entries]'
   ```

5. **Output**: Print flattened JSON to stdout

### 3. Data Transformation

**Before flattening:**
```json
{
  "cluster": {
    "name": "prod-cluster",
    "uuid": "abc-123"
  },
  "node": {
    "name": "node-01"
  }
}
```

**After flattening:**
```json
{
  "cluster_name": "prod-cluster",
  "cluster_uuid": "abc-123",
  "node_name": "node-01"
}
```

### 4. Event Creation
- Flex parses the JSON output from each script
- Creates New Relic events with the configured event type name
- Adds metadata (timestamp, host, etc.)

### 5. Data Transmission
- Events are batched and sent to New Relic via HTTPS
- Compressed using gzip for efficiency
- Includes New Relic license key for authentication

## Script Details

### NACluster.sh
- **Purpose**: Collect cluster-level configuration and status
- **API Endpoint**: `/api/cluster`
- **Output**: Single cluster object with configuration details
- **Metrics**: Cluster name, UUID, version, contact info

### NADisk.sh
- **Purpose**: Monitor disk inventory and health
- **API Endpoints**: 
  - `/api/storage/disks` (list)
  - `/api/storage/disks/{name}` (details)
- **Output**: Array of disk objects
- **Metrics**: Disk name, state, type, capacity, physical location

### NANode.sh
- **Purpose**: Track node health and performance
- **API Endpoints**: 
  - `/api/cluster/nodes` (list)
  - `/api/cluster/nodes/{uuid}` (details)
- **Output**: Array of node objects
- **Metrics**: Node name, state, uptime, model, version, HA status

### NAVol.sh
- **Purpose**: Monitor volume usage and configuration
- **API Endpoints**: 
  - `/api/storage/volumes` (list)
  - `/api/storage/volumes/{uuid}` (details)
- **Output**: Array of volume objects
- **Metrics**: Volume name, size, used space, state, type, encryption status

## Performance Considerations

### Polling Frequency
- Default: 30 seconds (configurable in flex-netapp.yml)
- Consider API rate limits on your NetApp cluster
- Balance freshness of data vs. API load

### Script Execution Time
- **NACluster.sh**: ~1-2 seconds (single API call)
- **NADisk.sh**: ~5-10 seconds (depends on disk count)
- **NANode.sh**: ~3-5 seconds (typically 2-4 nodes)
- **NAVol.sh**: ~10-30 seconds (depends on volume count)

### Resource Usage
- CPU: Low (primarily waiting on API responses)
- Memory: Moderate (stores JSON payloads in memory)
- Network: ~1-5 MB per poll cycle (depends on cluster size)

### Optimization Tips
1. **Increase polling interval** if you have many volumes/disks
2. **Selective monitoring**: Comment out scripts in flex-netapp.yml if not needed
3. **Parallel execution**: Scripts run in parallel by default via Flex
4. **API field filtering**: Use `fields=` parameter to request only needed data

## Security

### Authentication
- Uses HTTP Basic Authentication with Base64 encoding
- Credentials stored in shell script variables
- Future: Consider HashiCorp Vault or similar for credential management

### Communication
- HTTPS with TLS 1.2+
- Scripts use `-k` flag to skip certificate verification (for self-signed certs)
- **Production recommendation**: Install proper CA-signed certificates

### Permissions
- NetApp user should have read-only role
- Script files should have restricted permissions (700 or 750)
- Run as dedicated service account (not root)

## Troubleshooting Points

1. **Script fails**: Check stdout/stderr in Infrastructure agent logs
2. **Empty data**: Verify API connectivity and credentials
3. **Performance issues**: Check script execution time and polling frequency
4. **Data gaps**: Look for script timeouts or API throttling

## Alternative: NetAppOHI

The repository also includes a Python-based integration in `NetAppOHI/`:
- Uses Python instead of bash scripts
- Parses pre-generated output files instead of real-time API calls
- Different use case: Batch processing of NetApp CLI output

This is kept separate as an alternative approach for environments where:
- Direct API access is restricted
- NetApp CLI output is already being collected
- Python is preferred over bash

## Future Enhancements

- [ ] Environment variable support for credentials
- [ ] Certificate verification in production mode
- [ ] Rate limiting and backoff strategies
- [ ] Caching of UUID lists to reduce API calls
- [ ] Prometheus exporter compatibility
- [ ] Kubernetes deployment manifests
- [ ] Docker containerization
