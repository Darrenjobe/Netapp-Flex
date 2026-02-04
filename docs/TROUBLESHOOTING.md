# Troubleshooting Guide

This guide helps you diagnose and fix common issues with the NetApp Flex integration.

## Table of Contents

1. [No Data in New Relic](#no-data-in-new-relic)
2. [Script Execution Errors](#script-execution-errors)
3. [Authentication Issues](#authentication-issues)
4. [Network Connectivity Problems](#network-connectivity-problems)
5. [Performance Issues](#performance-issues)
6. [Data Quality Issues](#data-quality-issues)

---

## No Data in New Relic

### Symptom
NRQL queries return no results for NetApp event types.

### Diagnosis Steps

1. **Check if Infrastructure agent is running:**
```bash
sudo systemctl status newrelic-infra
```

2. **Check Infrastructure agent logs:**
```bash
sudo tail -f /var/log/newrelic-infra/newrelic-infra.log
```

3. **Search for Flex-related logs:**
```bash
sudo grep -i "nri-flex" /var/log/newrelic-infra/newrelic-infra.log | tail -20
```

4. **Search for NetApp-related logs:**
```bash
sudo grep -i "netapp" /var/log/newrelic-infra/newrelic-infra.log | tail -20
```

### Solutions

**If agent is not running:**
```bash
sudo systemctl start newrelic-infra
sudo systemctl enable newrelic-infra
```

**If Flex is not loading:**
- Verify flex-netapp.yml exists: `ls -l /etc/newrelic-infra/integrations.d/flex-netapp.yml`
- Check YAML syntax: `sudo cat /etc/newrelic-infra/integrations.d/flex-netapp.yml`
- Restart agent: `sudo systemctl restart newrelic-infra`

**If scripts are not executing:**
- Verify scripts exist and are executable
- Test manually (see [Script Execution Errors](#script-execution-errors))

---

## Script Execution Errors

### Symptom
Scripts don't produce output or produce errors when run manually.

### Test Each Script

```bash
# Test Cluster script
sudo /etc/newrelic-infra/integrations.d/NACluster.sh

# Test Disk script (may take longer)
sudo /etc/newrelic-infra/integrations.d/NADisk.sh | head -100

# Test Node script
sudo /etc/newrelic-infra/integrations.d/NANode.sh

# Test Volume script (may take longer)
sudo /etc/newrelic-infra/integrations.d/NAVol.sh | head -100
```

### Common Errors

#### Error: `command not found: jq`

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install jq

# RHEL/CentOS
sudo yum install jq

# Verify
jq --version
```

#### Error: `command not found: curl`

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install curl

# RHEL/CentOS
sudo yum install curl

# Verify
curl --version
```

#### Error: `Permission denied`

**Solution:**
```bash
sudo chmod +x /etc/newrelic-infra/integrations.d/NA*.sh
```

#### Error: Empty output or `null`

**Causes:**
- NetApp server unreachable
- Invalid credentials
- API returns empty results

**Diagnosis:**
```bash
# Check network connectivity
ping <NetAppServer>

# Test API directly
curl -X GET "https://<NetAppServer>/api/cluster" \
  -H "authorization: <AUTH>" \
  -k -s | jq '.'
```

---

## Authentication Issues

### Symptom
Scripts run but produce authentication errors or HTTP 401 responses.

### Diagnosis

1. **Test credentials directly:**
```bash
# Replace with your values
NETAPP_SERVER="your-netapp-cluster.example.com"
USERNAME="admin"
PASSWORD="yourpassword"

# Generate auth token
AUTH="Basic $(echo -n "${USERNAME}:${PASSWORD}" | base64)"

# Test
curl -X GET "https://${NETAPP_SERVER}/api/cluster" \
  -H "authorization: ${AUTH}" \
  -k -s | jq '.'
```

2. **Check for common auth issues:**
```bash
# Look for 401 errors in script output
sudo /etc/newrelic-infra/integrations.d/NACluster.sh 2>&1 | grep -i "401\|unauthorized\|auth"
```

### Solutions

**Invalid credentials:**
- Verify username and password
- Check if account is locked or expired
- Ensure account has API access permissions

**Incorrect AUTH format:**
```bash
# Correct format
AUTH="Basic $(echo -n 'username:password' | base64)"

# Common mistakes:
# - Missing 'Basic ' prefix
# - Using wrong encoding
# - Including newlines in base64
```

**Account lacks permissions:**
- NetApp user needs at least `readonly` role
- Verify in NetApp System Manager or CLI:
```bash
security login show -user-or-group-name <username>
```

---

## Network Connectivity Problems

### Symptom
Scripts timeout or fail to connect to NetApp cluster.

### Diagnosis

1. **Test basic connectivity:**
```bash
ping <NetAppServer>
```

2. **Test HTTPS connectivity:**
```bash
curl -k -v https://<NetAppServer>/api/cluster 2>&1 | grep -i "connect\|ssl\|timeout"
```

3. **Check firewall rules:**
```bash
# Test if port 443 is reachable
timeout 5 bash -c "</dev/tcp/<NetAppServer>/443" && echo "Port 443 is open" || echo "Port 443 is closed"
```

### Solutions

**Firewall blocking:**
- Open outbound HTTPS (port 443) from monitoring server to NetApp cluster
- Check both local firewall and network firewalls

**DNS resolution issues:**
- Use IP address instead of hostname in scripts
- Verify DNS: `nslookup <NetAppServer>`

**SSL/TLS issues:**
- Scripts use `-k` to skip certificate verification
- For production, install proper certificates:
```bash
# Update CA certificates
sudo update-ca-certificates  # Ubuntu/Debian
sudo update-ca-trust         # RHEL/CentOS
```

**Network timeouts:**
- Increase curl timeout in scripts (add `--max-time 30`)
- Check network latency: `ping -c 10 <NetAppServer>`

---

## Performance Issues

### Symptom
Scripts take too long to execute or timeout.

### Diagnosis

1. **Time script execution:**
```bash
time sudo /etc/newrelic-infra/integrations.d/NAVol.sh > /dev/null
```

2. **Check cluster size:**
```bash
# Count volumes
sudo /etc/newrelic-infra/integrations.d/NAVol.sh | jq '. | length'

# Count disks
sudo /etc/newrelic-infra/integrations.d/NADisk.sh | jq '. | length'
```

3. **Monitor resource usage:**
```bash
# While scripts are running
top -u root
```

### Solutions

**Too many resources:**
- Increase polling interval in flex-netapp.yml (e.g., 60 seconds instead of 30)
- Selective monitoring: Disable scripts you don't need

**Slow API responses:**
- Check NetApp cluster performance
- Consider using API field filtering to reduce response size
- Example: Add `?fields=name,uuid,state` to API URLs

**Memory issues:**
- Scripts load all data into memory before processing
- For very large clusters (1000+ volumes), consider batch processing

**Optimize jq processing:**
- The flattening operation can be slow for large datasets
- Consider simplifying the jq filter for better performance

---

## Data Quality Issues

### Symptom
Data appears in New Relic but is incomplete, incorrect, or inconsistent.

### Missing Metrics

**Check script output:**
```bash
sudo /etc/newrelic-infra/integrations.d/NAVol.sh | jq '.[0]'
```

**Common causes:**
- NetApp API doesn't return certain fields
- Fields are null or missing in NetApp
- jq filtering removes needed data

**Solution:**
- Modify scripts to request specific fields explicitly
- Example: Add `?fields=*` to get all available fields

### Incorrect Data Types

**Check JSON structure:**
```bash
sudo /etc/newrelic-infra/integrations.d/NACluster.sh | jq '.[0] | to_entries | map({key, type: (.value | type)})'
```

**Solution:**
- Ensure numeric values aren't quoted
- Modify jq filter if type conversion is needed

### Duplicate Events

**Symptoms:**
- Same data appears multiple times with different timestamps
- Double-counting in queries

**Causes:**
- Multiple Flex configurations running same scripts
- Scripts scheduled outside of Flex

**Solution:**
```bash
# Check for duplicate configs
sudo ls -l /etc/newrelic-infra/integrations.d/*netapp*.yml

# Check cron jobs
sudo crontab -l | grep -i netapp
```

---

## Getting Additional Help

### Enable Debug Logging

Edit `/etc/newrelic-infra.yml` and add:
```yaml
log:
  level: debug
```

Then restart:
```bash
sudo systemctl restart newrelic-infra
```

### Collect Diagnostic Information

```bash
# Infrastructure agent version
newrelic-infra --version

# Flex integration version
/var/db/newrelic-infra/newrelic-integrations/bin/nri-flex --version

# System information
uname -a

# Script checksums
md5sum /etc/newrelic-infra/integrations.d/NA*.sh

# Recent logs
sudo tail -100 /var/log/newrelic-infra/newrelic-infra.log
```

### Contact Support

When opening an issue, include:
1. Description of the problem
2. Error messages (if any)
3. Script output when run manually
4. Infrastructure agent logs
5. New Relic account ID (but NOT your license key)
6. NetApp ONTAP version

### Community Resources

- [GitHub Issues](https://github.com/Darrenjobe/Netapp-Flex/issues)
- [New Relic Community Forum](https://discuss.newrelic.com/)
- [NetApp Community](https://community.netapp.com/)
