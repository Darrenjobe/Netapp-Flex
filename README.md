# NetApp Flex Integration for New Relic

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![NetApp ONTAP](https://img.shields.io/badge/NetApp-ONTAP%209.6%2B-blue)](https://www.netapp.com/data-management/ontap-data-management-software/)
[![New Relic](https://img.shields.io/badge/New%20Relic-Flex-green)](https://docs.newrelic.com/docs/infrastructure/host-integrations/host-integrations-list/flex-integration-tool-build-your-own-integration/)

A production-ready monitoring solution for NetApp ONTAP storage systems using New Relic's Flex integration. Collect real-time metrics on clusters, nodes, disks, and volumes through the NetApp REST API.

## 📋 Overview

This integration enables comprehensive monitoring of NetApp storage infrastructure by collecting metrics directly from the ONTAP REST API and forwarding them to New Relic for analysis, visualization, and alerting.

### Key Capabilities

- 🔄 **Real-time Monitoring** - Continuous data collection at configurable intervals
- 📊 **Comprehensive Metrics** - Cluster, node, disk, and volume statistics
- 🚀 **Easy Deployment** - Simple shell scripts with minimal dependencies
- 🔒 **Secure Communication** - HTTPS with authentication
- 📈 **New Relic Integration** - Native event format for NRQL queries
- 🛠️ **Low Maintenance** - No agents on NetApp systems required

### Collected Metrics

| Category | Metrics | Event Type |
|----------|---------|------------|
| **Volumes** | Size, used space, available space, inode usage, state, type, encryption | `NetAppVolSample` |
| **Cluster** | Name, version, UUID, contact info, location, serial number | `NetAppClusterSample` |
| **Disks** | Name, type, capacity, state, firmware, physical location, container | `NetAppDiskSample` |
| **Nodes** | Name, state, uptime, model, serial number, CPU, memory, HA status | `NetAppNodeSample` |

## 🚀 Quick Start

### Prerequisites

- New Relic account with Infrastructure agent installed
- New Relic Flex integration
- NetApp ONTAP 9.6 or later
- `curl`, `jq`, and `bash`

### Installation

```bash
# Clone the repository
git clone https://github.com/Darrenjobe/Netapp-Flex.git
cd Netapp-Flex

# Configure credentials in scripts/NA*.sh
# Update NetAppServer and AUTH variables

# Deploy scripts
sudo cp scripts/*.sh /etc/newrelic-infra/integrations.d/
sudo chmod +x /etc/newrelic-infra/integrations.d/NA*.sh

# Deploy configuration
sudo cp config/flex-netapp.yml /etc/newrelic-infra/integrations.d/

# Restart New Relic Infrastructure agent
sudo systemctl restart newrelic-infra
```

### Verify Installation

```bash
# Test scripts manually
sudo /etc/newrelic-infra/integrations.d/NACluster.sh | jq '.'

# Query data in New Relic (after 1-2 minutes)
# Run in New Relic One → Query your data
SELECT * FROM NetAppVolSample SINCE 5 minutes ago LIMIT 10
```

📚 **Detailed Instructions:** See [Installation Guide](docs/INSTALLATION.md)

## 📁 Project Structure

```
Netapp-Flex/
├── scripts/              # Shell scripts for data collection
│   ├── NACluster.sh     # Cluster configuration and metadata
│   ├── NADisk.sh        # Disk inventory and health
│   ├── NANode.sh        # Node health and performance
│   └── NAVol.sh         # Volume usage and configuration
├── config/              # Configuration files
│   └── flex-netapp.yml  # New Relic Flex integration config
├── docs/                # Documentation
│   ├── INSTALLATION.md  # Detailed installation guide
│   ├── ARCHITECTURE.md  # Architecture and data flow
│   └── TROUBLESHOOTING.md # Common issues and solutions
├── examples/            # Example configurations
│   └── flex-netapp-example.yml
├── NetAppOHI/          # Alternative Python-based integration
│   ├── custom-integrations/
│   └── integrations.d/
└── README.md           # This file
```

## 🔧 Configuration

### Authentication

Edit each script in `scripts/` and update:

```bash
NetAppServer=your-netapp-cluster.example.com
AUTH=<YOUR_AUTH_TOKEN>
```

Generate AUTH token:
```bash
AUTH="Basic $(echo -n 'username:password' | base64)"
```

### Polling Interval

Modify `config/flex-netapp.yml` to adjust collection frequency. Default is every 30 seconds.

### Selective Monitoring

Comment out scripts in `config/flex-netapp.yml` that you don't need:

```yaml
# Disable disk monitoring
# - name: NetAppDisk
#   commands:
#     - run: /etc/newrelic-infra/integrations.d/NADisk.sh
```

## 📊 Data Examples

### Volume Metrics
```json
{
  "uuid": "abc-123-def-456",
  "name": "vol_prod_data",
  "size": 1099511627776,
  "space_used": 824633720832,
  "space_available": 274877906944,
  "state": "online",
  "type": "rw",
  "is_svm_root": false
}
```

### Cluster Information
```json
{
  "uuid": "cluster-uuid-123",
  "name": "prod-cluster",
  "version_full": "NetApp Release 9.12.1",
  "contact": "admin@example.com",
  "location": "Datacenter A"
}
```

## 📈 New Relic Queries

### Monitor Volume Capacity

```sql
-- Volumes over 80% capacity
SELECT name, (space_used / size * 100) AS usedPercent 
FROM NetAppVolSample 
WHERE (space_used / size * 100) > 80 
SINCE 1 hour ago
```

### Check Disk Health

```sql
-- Non-healthy disks
SELECT name, state, container_type 
FROM NetAppDiskSample 
WHERE state != 'healthy' 
SINCE 1 day ago
```

### Node Uptime

```sql
-- Node uptime monitoring
SELECT name, uptime, state 
FROM NetAppNodeSample 
SINCE 1 hour ago
```

### Volume Growth Trend

```sql
-- Volume usage over time
SELECT average(space_used / size * 100) 
FROM NetAppVolSample 
FACET name 
TIMESERIES AUTO 
SINCE 7 days ago
```

## 🏗️ Architecture

The integration uses a simple, efficient architecture:

1. **New Relic Flex** reads `flex-netapp.yml` and executes scripts on schedule
2. **Shell Scripts** query NetApp ONTAP REST API using `curl`
3. **Data Processing** flattens nested JSON using `jq` for easy parsing
4. **Event Creation** Flex converts JSON to New Relic events
5. **Data Storage** Events stored in New Relic database (NRDB)

```
NetApp ONTAP ─(REST API)→ Shell Scripts ─(JSON)→ Flex ─(HTTPS)→ New Relic
```

📚 **Detailed Architecture:** See [Architecture Documentation](docs/ARCHITECTURE.md)

## 🔒 Security Best Practices

- ✅ Use read-only NetApp accounts for monitoring
- ✅ Never commit credentials to version control
- ✅ Restrict file permissions on scripts (700 or 750)
- ✅ Use proper SSL certificates in production (remove `-k` flag)
- ✅ Regularly rotate credentials
- ✅ Monitor access logs on NetApp clusters
- ✅ Use dedicated service accounts (not root)

## 🛠️ Troubleshooting

### Common Issues

| Issue | Quick Fix |
|-------|----------|
| No data in New Relic | Check agent logs: `sudo tail -f /var/log/newrelic-infra/newrelic-infra.log` |
| Empty script output | Verify credentials and network connectivity |
| `jq: command not found` | Install jq: `sudo apt-get install jq` or `sudo yum install jq` |
| Permission denied | `sudo chmod +x /etc/newrelic-infra/integrations.d/NA*.sh` |
| Slow performance | Increase polling interval or disable unneeded scripts |

📚 **Comprehensive Guide:** See [Troubleshooting Documentation](docs/TROUBLESHOOTING.md)

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION.md) - Step-by-step installation instructions
- [Architecture](docs/ARCHITECTURE.md) - System design and data flow
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🐛 **Report bugs** - Open an issue with details
2. 💡 **Suggest features** - Share your ideas
3. 🔧 **Submit pull requests** - Fix bugs or add features
4. 📖 **Improve documentation** - Help others understand
5. ⭐ **Star the repository** - Show your support

### Development

```bash
# Clone for development
git clone https://github.com/Darrenjobe/Netapp-Flex.git
cd Netapp-Flex

# Test scripts locally
bash scripts/NACluster.sh | jq '.'

# Validate YAML
yamllint config/flex-netapp.yml
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Resources

- [NetApp ONTAP REST API Documentation](https://docs.netapp.com/us-en/ontap-automation/)
- [New Relic Flex Integration Guide](https://docs.newrelic.com/docs/infrastructure/host-integrations/host-integrations-list/flex-integration-tool-build-your-own-integration/)
- [New Relic Infrastructure Agent](https://docs.newrelic.com/docs/infrastructure/install-infrastructure-agent/)
- [NRQL Query Language](https://docs.newrelic.com/docs/query-your-data/nrql-new-relic-query-language/get-started/introduction-nrql-new-relics-query-language/)

## 👤 Author

**Darren Jobe**

- GitHub: [@Darrenjobe](https://github.com/Darrenjobe)
- Repository: [Netapp-Flex](https://github.com/Darrenjobe/Netapp-Flex)

## ⭐ Support

If this project helps you, please consider giving it a ⭐ star on GitHub!

---

## 🆚 Alternative: NetAppOHI

This repository also includes an alternative Python-based integration in the `NetAppOHI/` directory. This approach:

- Uses Python instead of shell scripts
- Processes pre-generated NetApp CLI output files
- Suitable for environments where direct API access is restricted

Choose the shell script approach (recommended) for real-time monitoring via REST API, or the Python approach for batch processing of CLI output.

---

**Note:** Remember to configure `NetAppServer` and `AUTH` variables in all scripts before deployment. Never commit actual credentials to version control.
