# Contributing to NetApp Flex Integration

Thank you for your interest in contributing to the NetApp Flex Integration project! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Issues

If you encounter a bug or have a suggestion:

1. **Check existing issues** - Search [GitHub Issues](https://github.com/Darrenjobe/Netapp-Flex/issues) to see if it's already reported
2. **Create a detailed report** - Include:
   - Clear description of the issue or enhancement
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Environment details (OS, New Relic agent version, NetApp ONTAP version)
   - Error messages or logs (redact sensitive information)
   - Screenshots if applicable

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:

1. Open an issue with the `enhancement` label
2. Describe the feature and its benefits
3. Explain the use case
4. Provide examples if possible

### Pull Requests

We love pull requests! Here's the process:

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/Netapp-Flex.git
   cd Netapp-Flex
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make your changes**
   - Follow the code style guidelines (see below)
   - Add or update tests if applicable
   - Update documentation as needed

4. **Test your changes**
   ```bash
   # Test scripts manually
   bash scripts/NACluster.sh | jq '.'
   bash scripts/NADisk.sh | jq '.' | head -50
   bash scripts/NANode.sh | jq '.'
   bash scripts/NAVol.sh | jq '.' | head -50
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template with details

## 📝 Code Style Guidelines

### Shell Scripts

- **Shebang**: Use `#!/usr/bin/env bash` for portability
- **Variables**: 
  - Use PascalCase for API-related variables: `NetAppServer`, `AUTH`
  - Use UPPER_CASE for payload variables: `VOL_PAYLOAD`, `DISK_PAYLOAD`
  - Quote variables: `"$VARIABLE"` to handle spaces
- **Comments**: 
  - Add comments explaining complex logic
  - Use `#` for single-line comments
- **Error Handling**:
  - Add error checks for critical operations
  - Provide meaningful error messages
- **Formatting**:
  - Use 4 spaces for indentation
  - Add blank lines between logical sections

Example:
```bash
#!/usr/bin/env bash

# Variable Declaration
NetAppServer=<SERVER>
AUTH=<AUTH>
VOL_PAYLOAD=''

# Hitting the first endpoint to pull a list of Volume UUIDs
VOLS_RAW=$(curl -X GET "https://$NetAppServer/api/storage/volumes" \
    -H "accept: application/json" \
    -H "authorization: $AUTH" \
    -k -s)
```

### YAML Configuration

- **Indentation**: Use 2 spaces (no tabs)
- **Comments**: Add comments to explain configuration options
- **Formatting**: Align values for readability

Example:
```yaml
integrations:
  - name: nri-flex
    config:
      name: netAppSample
      apis:
        # Volume metrics collection
        - name: NetAppVol
          commands:
            - run: /etc/newrelic-infra/integrations.d/NAVol.sh
```

### Markdown Documentation

- **Headers**: Use ATX-style headers (`#`, `##`, `###`)
- **Code blocks**: Always specify language for syntax highlighting
- **Links**: Use descriptive link text
- **Lists**: Use `-` for unordered lists, numbers for ordered lists
- **Tables**: Align columns for readability in source

## 🧪 Testing Guidelines

### Manual Testing

Before submitting a PR, test:

1. **Script execution**: Run each modified script independently
2. **JSON output**: Verify output is valid JSON using `jq`
3. **API connectivity**: Ensure scripts work with a real NetApp cluster
4. **Error cases**: Test with invalid credentials, unreachable servers

### Test Checklist

- [ ] Scripts execute without errors
- [ ] JSON output is valid and well-formed
- [ ] No credentials are hardcoded or committed
- [ ] Scripts handle errors gracefully
- [ ] Documentation is updated
- [ ] Examples are working and clear

## 📚 Documentation Standards

### README Updates

If your change affects user-facing functionality:

- Update the README.md
- Add examples if introducing new features
- Update the Quick Start if installation changes

### Documentation Files

- Keep docs in the `docs/` directory
- Use clear, concise language
- Include examples and code snippets
- Add troubleshooting tips for common issues

### Code Comments

- Explain **why**, not **what** (the code shows what)
- Document complex algorithms or workarounds
- Add TODO comments for future improvements

## 🔒 Security Guidelines

### Do Not Commit Credentials

- Never commit actual NetApp credentials
- Use placeholder values like `<SERVER>` and `<AUTH>`
- Check commits before pushing: `git diff --cached`

### Security Vulnerabilities

If you discover a security vulnerability:

1. **Do not** open a public issue
2. Email the maintainer privately
3. Provide details and proof of concept
4. Wait for acknowledgment before disclosure

## 🏷️ Commit Message Guidelines

Use clear, descriptive commit messages:

```
Add feature: Support for NetApp Snapshots API

- Add NASnapshot.sh script to collect snapshot metrics
- Update flex-netapp.yml with new snapshot endpoint
- Add documentation for snapshot monitoring
- Include example NRQL queries for snapshots
```

Format:
- First line: Brief summary (50 characters or less)
- Blank line
- Detailed explanation if needed (wrap at 72 characters)
- Bullet points for multiple changes

### Commit Message Types

- `Add feature:` - New functionality
- `Fix:` - Bug fixes
- `Update:` - Changes to existing features
- `Refactor:` - Code restructuring
- `Docs:` - Documentation only
- `Style:` - Formatting changes
- `Test:` - Adding or updating tests

## 🎯 Areas for Contribution

### High Priority

- Environment variable support for credentials
- Certificate verification in production mode
- Rate limiting and backoff strategies
- Additional NetApp API endpoints (aggregates, SVMs, snapshots)
- Performance optimizations

### Medium Priority

- Docker containerization
- Kubernetes deployment manifests
- Prometheus exporter compatibility
- Dashboard templates for New Relic
- Alert policy examples

### Documentation

- Video tutorials
- Blog posts
- Use case examples
- Comparison with other monitoring solutions
- Best practices guide

## 🌟 Recognition

Contributors will be:

- Listed in the project's contributors
- Mentioned in release notes
- Credited in documentation for significant contributions

## ❓ Questions?

If you have questions about contributing:

1. Check existing documentation
2. Search closed issues for similar questions
3. Open a new issue with the `question` label
4. Reach out to the maintainer

## 📜 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Personal attacks
- Publishing others' private information
- Other conduct inappropriate in a professional setting

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to NetApp Flex Integration! 🎉
