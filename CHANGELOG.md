# Changelog

All notable changes to the NetApp Flex Integration project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive project reorganization with proper directory structure
- `scripts/` directory containing all shell scripts (NACluster.sh, NADisk.sh, NANode.sh, NAVol.sh)
- `config/` directory for configuration files
- `docs/` directory with detailed documentation:
  - INSTALLATION.md - Step-by-step installation guide
  - ARCHITECTURE.md - System design and data flow documentation
  - TROUBLESHOOTING.md - Common issues and solutions
- `examples/` directory with example configurations
- CONTRIBUTING.md - Guidelines for contributors
- LICENSE - MIT License
- .gitignore - Prevent accidental commits of sensitive files
- Enhanced README.md with badges, better structure, and comprehensive examples

### Changed
- Moved all shell scripts from root to `scripts/` directory
- Moved flex-netapp.yml from root to `config/` directory
- Completely rewrote README.md with modern formatting and comprehensive documentation
- Updated flex-netapp.yml with better comments and formatting

### Improved
- Documentation is now more comprehensive and better organized
- Project structure follows industry best practices
- Security guidance is more prominent
- Installation instructions are clearer and more detailed
- Added numerous NRQL query examples
- Better visual hierarchy with emojis and badges

## [1.0.0] - Prior to reorganization

### Initial Release
- Shell scripts for NetApp ONTAP monitoring
  - NACluster.sh - Cluster metrics
  - NADisk.sh - Disk inventory
  - NANode.sh - Node health
  - NAVol.sh - Volume metrics
- Flex configuration file (flex-netapp.yml)
- Alternative Python-based integration (NetAppOHI)
- Basic README documentation

[Unreleased]: https://github.com/Darrenjobe/Netapp-Flex/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Darrenjobe/Netapp-Flex/releases/tag/v1.0.0
