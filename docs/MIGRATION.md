# Migration Guide: Old Structure to New Structure

This document helps users who were using the old project structure migrate to the new, reorganized structure.

## What Changed?

The project has been reorganized for better maintainability and clarity. Here's a comparison:

### Old Structure (Before)
```
Netapp-Flex/
├── NACluster.sh
├── NADisk.sh
├── NANode.sh
├── NAVol.sh
├── flex-netapp.yml
├── NetAppOHI/
└── README.md
```

### New Structure (After)
```
Netapp-Flex/
├── scripts/
│   ├── NACluster.sh
│   ├── NADisk.sh
│   ├── NANode.sh
│   └── NAVol.sh
├── config/
│   └── flex-netapp.yml
├── docs/
│   ├── INSTALLATION.md
│   ├── ARCHITECTURE.md
│   └── TROUBLESHOOTING.md
├── examples/
│   └── flex-netapp-example.yml
├── NetAppOHI/
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── .gitignore
└── README.md (completely rewritten)
```

## File Locations

| Old Location | New Location | Notes |
|--------------|--------------|-------|
| `NACluster.sh` | `scripts/NACluster.sh` | Moved to scripts directory |
| `NADisk.sh` | `scripts/NADisk.sh` | Moved to scripts directory |
| `NANode.sh` | `scripts/NANode.sh` | Moved to scripts directory |
| `NAVol.sh` | `scripts/NAVol.sh` | Moved to scripts directory |
| `flex-netapp.yml` | `config/flex-netapp.yml` | Moved to config directory, improved comments |
| `README.md` | `README.md` | Completely rewritten with better structure |
| N/A | `docs/INSTALLATION.md` | New detailed installation guide |
| N/A | `docs/ARCHITECTURE.md` | New architecture documentation |
| N/A | `docs/TROUBLESHOOTING.md` | New troubleshooting guide |
| N/A | `examples/flex-netapp-example.yml` | New example configuration |
| N/A | `CONTRIBUTING.md` | New contribution guidelines |
| N/A | `LICENSE` | New MIT License file |
| N/A | `CHANGELOG.md` | New changelog |
| N/A | `.gitignore` | New gitignore for security |

## Migration Steps

### If You're Running the Integration

**Good news!** You don't need to do anything. The scripts and configuration on your New Relic Infrastructure server remain unchanged. This reorganization only affects the repository structure, not the deployed files.

### If You Have a Fork or Clone

1. **Pull the latest changes:**
   ```bash
   cd Netapp-Flex
   git fetch origin
   git pull origin main
   ```

2. **Update any custom scripts or automation:**
   - If you have scripts that reference file paths, update them:
     - `NACluster.sh` → `scripts/NACluster.sh`
     - `flex-netapp.yml` → `config/flex-netapp.yml`

3. **Review new documentation:**
   - Check out the new `docs/` directory for comprehensive guides
   - Update any internal documentation to reference new paths

### If You're Deploying Fresh

Follow the updated installation instructions in [docs/INSTALLATION.md](docs/INSTALLATION.md).

The deployment process is now clearer:

```bash
# Clone the repository
git clone https://github.com/Darrenjobe/Netapp-Flex.git
cd Netapp-Flex

# Configure credentials in scripts/NA*.sh
# Deploy scripts from new location
sudo cp scripts/*.sh /etc/newrelic-infra/integrations.d/
sudo chmod +x /etc/newrelic-infra/integrations.d/NA*.sh

# Deploy configuration from new location
sudo cp config/flex-netapp.yml /etc/newrelic-infra/integrations.d/

# Restart agent
sudo systemctl restart newrelic-infra
```

## What's Improved?

### 1. Better Organization
- Scripts are now in a dedicated `scripts/` directory
- Configuration files are in `config/`
- Documentation is organized in `docs/`
- Examples are in `examples/`

### 2. Comprehensive Documentation
- **INSTALLATION.md**: Step-by-step installation guide with troubleshooting
- **ARCHITECTURE.md**: Deep dive into how the integration works
- **TROUBLESHOOTING.md**: Solutions to common problems
- **CONTRIBUTING.md**: Guidelines for contributors

### 3. Enhanced README
- Professional badges
- Clear structure with emojis
- Quick start guide
- NRQL query examples
- Better security guidance
- Project structure visualization

### 4. Security Improvements
- `.gitignore` prevents accidental credential commits
- Enhanced security best practices in documentation
- Clear guidance on credential management

### 5. Project Management
- `LICENSE` file (MIT License)
- `CHANGELOG.md` for tracking changes
- `CONTRIBUTING.md` for community contributions

## Breaking Changes

**None!** This reorganization is **non-breaking** for existing deployments.

- Deployed scripts continue to work as-is
- API endpoints are unchanged
- Script logic is unchanged
- Configuration format is unchanged (just improved comments)

## Questions?

If you have questions about the migration:

1. Check the [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) guide
2. Review the [INSTALLATION.md](docs/INSTALLATION.md) guide
3. Open an issue on GitHub
4. Check the [CONTRIBUTING.md](CONTRIBUTING.md) for how to get help

## Feedback

We'd love to hear your feedback on the new structure! 

- Is it clearer?
- Is the documentation helpful?
- What else would you like to see?

Open an issue or discussion on GitHub to share your thoughts.

---

**Thank you for using NetApp Flex Integration!** 🎉
