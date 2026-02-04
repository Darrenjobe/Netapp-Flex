# NetApp Flex Integration

A comprehensive monitoring solution for NetApp storage systems using New Relic's Flex integration. This project provides shell scripts to collect and format NetApp cluster, disk, volume, and node metrics through the NetApp ONTAP REST API.

## 📋 Overview

This integration collects real-time metrics from NetApp storage systems and forwards them to New Relic for monitoring and analysis. It leverages the NetApp ONTAP REST API to retrieve detailed information about:

- **Clusters** - Cluster configuration and status
- **Disks** - Storage disk inventory and health
- **Volumes** - Volume usage and performance metrics
- **Nodes** - Node health, uptime, and system information

## 🚀 Features

- Real-time data collection from NetApp ONTAP REST API
- JSON output formatted for New Relic Flex integration
- Automated polling of multiple NetApp resources
- Clean, flattened JSON structure for easy metric parsing
- Secure HTTPS communication with NetApp controllers

## 📦 Components

### Shell Scripts

| Script | Description |
|--------|-------------|
| `NACluster.sh` | Retrieves cluster configuration and metadata |
| `NADisk.sh` | Collects storage disk inventory and status |
| `NANode.sh` | Gathers node health, performance, and system information |
| `NAVol.sh` | Retrieves volume metrics including usage and configuration |

### Configuration

- `flex-netapp.yml` - New Relic Flex integration configuration file

## 🔧 Prerequisites

- New Relic Infrastructure agent installed
- New Relic Flex integration installed
- Access to NetApp ONTAP REST API
- Required tools:
  - `curl`
  - `jq` (JSON processor)
  - `bash`

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Darrenjobe/Netapp-Flex.git
cd Netapp-Flex
```

### 2. Configure NetApp Credentials

Edit each shell script (`NACluster.sh`, `NADisk.sh`, `NANode.sh`, `NAVol.sh`) and update the following variables:

```bash
NetAppServer=<YOUR_NETAPP_SERVER>
AUTH=<YOUR_AUTH_TOKEN>
```

**Authentication Format:** Use Basic Authentication encoded in Base64:
```bash
AUTH="Basic $(echo -n 'username:password' | base64)"
```

### 3. Deploy Scripts

Copy the scripts to the New Relic integrations directory:

```bash
sudo cp *.sh /etc/newrelic-infra/integrations.d/
sudo chmod +x /etc/newrelic-infra/integrations.d/NA*.sh
```

### 4. Deploy Flex Configuration

Copy the Flex configuration file:

```bash
sudo cp flex-netapp.yml /etc/newrelic-infra/integrations.d/
```

### 5. Restart New Relic Infrastructure Agent

```bash
sudo systemctl restart newrelic-infra
```

## 🔍 How It Works

### Data Collection Flow

1. **Initial API Call** - Each script makes an initial API call to retrieve a list of resource UUIDs
2. **Iteration** - Scripts iterate through each UUID to fetch detailed information
3. **Aggregation** - Response data is aggregated into a single JSON payload
4. **Transformation** - JSON is flattened using `jq` for easier metric parsing
5. **Output** - Formatted JSON is output to stdout for Flex to consume

### Example: Volume Collection Process

```bash
# 1. Get list of volume UUIDs
VOLS=$(curl .../api/storage/volumes | jq '.records[].uuid')

# 2. Loop through each volume
for VOL in $VOLS; do
    RESPONSE=$(curl .../api/storage/volumes/$VOL)
    VOL_PAYLOAD=$(echo "$RESPONSE" "$VOL_PAYLOAD" | jq -s '.')
done

# 3. Flatten and output
echo $VOL_PAYLOAD | jq '[.[] | flatten]'
```

## 📊 Data Structure

All scripts output flattened JSON with nested keys joined by underscores:

```json
[
  {
    "cluster_uuid": "abc-123",
    "cluster_name": "prod-cluster",
    "node_uuid": "def-456",
    "node_name": "node-01",
    "metric_duration": "PT15S"
  }
]
```

## 🔒 Security Considerations

- **Credentials**: Never commit actual credentials to version control
- **HTTPS**: Scripts use `-k` flag to skip SSL verification (remove in production with valid certs)
- **API Access**: Ensure the NetApp user account has appropriate read-only permissions
- **File Permissions**: Restrict script access with appropriate file permissions

## 🛠️ Troubleshooting

### Test Scripts Manually

Run scripts individually to verify connectivity:

```bash
sudo /etc/newrelic-infra/integrations.d/NACluster.sh
```

### Check New Relic Logs

```bash
sudo tail -f /var/log/newrelic-infra/newrelic-infra.log
```

### Verify jq Installation

```bash
which jq
jq --version
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Empty output | Check NetApp credentials and server connectivity |
| `jq` command not found | Install jq: `sudo apt-get install jq` or `sudo yum install jq` |
| Permission denied | Ensure scripts have execute permissions: `chmod +x *.sh` |
| SSL errors | Update certificates or temporarily use `-k` flag for testing |

## 📈 New Relic Queries

Once data is flowing, query your NetApp metrics in New Relic:

```sql
-- View all NetApp volumes
SELECT * FROM NetAppVolSample SINCE 1 hour ago

-- Check cluster health
SELECT * FROM NetAppClusterSample SINCE 30 minutes ago

-- Monitor disk status
SELECT * FROM NetAppDiskSample WHERE state != 'healthy' SINCE 1 day ago

-- Node performance
SELECT * FROM NetAppNodeSample SINCE 1 hour ago
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📝 License

This project is provided as-is for monitoring NetApp storage systems with New Relic.

## 🔗 Resources

- [NetApp ONTAP REST API Documentation](https://docs.netapp.com/us-en/ontap-automation/)
- [New Relic Flex Integration](https://docs.newrelic.com/docs/infrastructure/host-integrations/host-integrations-list/flex-integration-tool-build-your-own-integration/)
- [New Relic Infrastructure Agent](https://docs.newrelic.com/docs/infrastructure/install-infrastructure-agent/)

## 👤 Author

**Darrenjobe**
- GitHub: [@Darrenjobe](https://github.com/Darrenjobe)

---

**Note:** Remember to replace `<SERVER>` and `<AUTH>` placeholders in all scripts before deployment.
