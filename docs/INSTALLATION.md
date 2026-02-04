# Installation Guide

This guide walks you through installing and configuring the NetApp Flex integration for New Relic.

## Prerequisites

Before you begin, ensure you have:

- [ ] New Relic Infrastructure agent installed and running
- [ ] New Relic Flex integration installed
- [ ] Access to NetApp ONTAP REST API (v9.6 or later)
- [ ] NetApp user account with appropriate read permissions
- [ ] Required system tools:
  - `curl` - for API calls
  - `jq` - for JSON processing
  - `bash` - for script execution

## Step 1: Verify Prerequisites

### Check New Relic Infrastructure Agent

```bash
sudo systemctl status newrelic-infra
```

### Check New Relic Flex Integration

```bash
ls /var/db/newrelic-infra/newrelic-integrations/bin/nri-flex
```

### Install jq (if not present)

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install jq
```

**RHEL/CentOS:**
```bash
sudo yum install jq
```

**Verify installation:**
```bash
jq --version
```

## Step 2: Clone the Repository

```bash
git clone https://github.com/Darrenjobe/Netapp-Flex.git
cd Netapp-Flex
```

## Step 3: Configure NetApp Credentials

You need to configure authentication for each script. There are two approaches:

### Option A: Edit Scripts Directly

Edit each script in the `scripts/` directory and update these variables:

```bash
NetAppServer=<YOUR_NETAPP_CLUSTER_MGMT_IP>
AUTH=<YOUR_AUTH_TOKEN>
```

**Generate AUTH token:**
```bash
# Replace username and password with your NetApp credentials
AUTH="Basic $(echo -n 'admin:yourpassword' | base64)"
```

### Option B: Use Environment Variables (Recommended)

Modify the scripts to read from environment variables:

1. Create a credentials file (keep secure, never commit!):
```bash
sudo nano /etc/newrelic-infra/netapp-credentials.env
```

2. Add your credentials:
```bash
NETAPP_SERVER=your-netapp-cluster.example.com
NETAPP_USERNAME=admin
NETAPP_PASSWORD=yourpassword
```

3. Secure the file:
```bash
sudo chmod 600 /etc/newrelic-infra/netapp-credentials.env
sudo chown root:root /etc/newrelic-infra/netapp-credentials.env
```

## Step 4: Deploy Scripts

Copy the scripts to the New Relic integrations directory:

```bash
sudo cp scripts/*.sh /etc/newrelic-infra/integrations.d/
sudo chmod +x /etc/newrelic-infra/integrations.d/NA*.sh
```

**Verify:**
```bash
ls -l /etc/newrelic-infra/integrations.d/NA*.sh
```

## Step 5: Deploy Configuration

Copy the Flex configuration file:

```bash
sudo cp config/flex-netapp.yml /etc/newrelic-infra/integrations.d/
```

**Verify:**
```bash
cat /etc/newrelic-infra/integrations.d/flex-netapp.yml
```

## Step 6: Test Scripts Manually

Before restarting the agent, test each script individually:

```bash
sudo /etc/newrelic-infra/integrations.d/NACluster.sh | jq '.'
sudo /etc/newrelic-infra/integrations.d/NADisk.sh | jq '.' | head -50
sudo /etc/newrelic-infra/integrations.d/NANode.sh | jq '.'
sudo /etc/newrelic-infra/integrations.d/NAVol.sh | jq '.' | head -50
```

**Expected output:** Valid JSON with NetApp metrics. If you see errors:
- Check NetApp credentials
- Verify network connectivity to NetApp cluster
- Ensure NetApp REST API is accessible

## Step 7: Restart New Relic Infrastructure Agent

```bash
sudo systemctl restart newrelic-infra
```

**Verify it's running:**
```bash
sudo systemctl status newrelic-infra
```

## Step 8: Verify Data in New Relic

Wait 1-2 minutes for data to start flowing, then check in New Relic:

1. Go to New Relic One → Query your data
2. Run this NRQL query:

```sql
SELECT * FROM NetAppVolSample SINCE 5 minutes ago LIMIT 10
```

You should see NetApp volume data. Try these queries too:

```sql
SELECT * FROM NetAppClusterSample SINCE 5 minutes ago
SELECT * FROM NetAppDiskSample SINCE 5 minutes ago
SELECT * FROM NetAppNodeSample SINCE 5 minutes ago
```

## Troubleshooting

### No data appearing in New Relic

1. **Check Infrastructure agent logs:**
```bash
sudo tail -f /var/log/newrelic-infra/newrelic-infra.log | grep -i netapp
```

2. **Check for errors:**
```bash
sudo grep -i error /var/log/newrelic-infra/newrelic-infra.log
```

3. **Verify Flex is running the scripts:**
```bash
sudo grep -i "nri-flex" /var/log/newrelic-infra/newrelic-infra.log
```

### Scripts produce empty output

- Verify NetApp credentials are correct
- Check network connectivity: `ping <NetApp_Server>`
- Test API directly:
```bash
curl -X GET "https://<NetApp_Server>/api/cluster" \
  -H "authorization: Basic <base64_auth>" \
  -k -s | jq '.'
```

### SSL Certificate errors

If you see SSL errors and trust your NetApp certificate:
- The scripts already use `-k` flag to skip verification
- For production, install proper SSL certificates on NetApp

### Permission denied errors

```bash
sudo chmod +x /etc/newrelic-infra/integrations.d/NA*.sh
```

## Next Steps

- Set up dashboards in New Relic to visualize your NetApp data
- Configure alerts for critical metrics (disk failures, high volume usage, etc.)
- Review the [Troubleshooting Guide](TROUBLESHOOTING.md) for common issues
- Explore the [New Relic NRQL documentation](https://docs.newrelic.com/docs/query-your-data/nrql-new-relic-query-language/get-started/introduction-nrql-new-relics-query-language/)

## Security Best Practices

- Never commit credentials to version control
- Use read-only NetApp accounts for monitoring
- Regularly rotate credentials
- Restrict file permissions on script files and credentials
- Use HTTPS with valid certificates in production
- Monitor access logs on your NetApp cluster
