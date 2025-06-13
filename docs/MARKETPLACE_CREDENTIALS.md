# 🔐 Marketplace Publishing & Credentials Guide

## 📋 **Publisher Identity (Opius AI)**

- **Company Name**: Opius AI
- **Extension Name**: opius-planner
- **Publisher ID**: opius-ai (where applicable)
- **Contact Email**: marketplace@opius.ai
- **Support Email**: support@opius.ai
- **Website**: https://opius.ai

## 🏪 **Marketplace Account Setup Guide**

### **VS Code Marketplace**
```markdown
# VS Code Marketplace Setup

## Required Accounts
1. **Microsoft Account** (free)
   - Go to: https://dev.azure.com
   - Sign up with opius.ai email
   - Create organization: "Opius AI"

2. **Publisher Registration**
   - Go to: https://marketplace.visualstudio.com/manage
   - Create publisher: "opius-ai"
   - Display name: "Opius AI"
   - Verify email and domain

## Required Information
- **Company Logo**: 128x128 PNG (opius-ai-logo.png)
- **Extension Icon**: 128x128 PNG (opius-planner-icon.png)
- **Company Description**: "Opius AI builds intelligent planning and automation tools"
- **Support URL**: https://support.opius.ai
- **Privacy Policy**: https://opius.ai/privacy
- **License**: MIT

## Verification Steps
- [ ] Email verification completed
- [ ] Domain verification (opius.ai)
- [ ] Publisher profile completed
- [ ] Payment method added (for paid features)
```

### **Cursor Marketplace**
```markdown
# Cursor Marketplace Setup

## Required Information
- **Company**: Opius AI
- **Extension ID**: opius-planner
- **Contact**: cursor-marketplace@opius.ai
- **Website**: https://opius.ai

## Submission Process
1. Contact Cursor team for publisher onboarding
2. Submit extension package
3. Provide company verification documents
4. Complete security review
```

### **Windsurf Marketplace**
```markdown
# Windsurf Marketplace Setup

## Required Information
- **Publisher**: Opius AI
- **Extension Name**: Opius Planner
- **Category**: Planning & Productivity
- **Contact**: windsurf-marketplace@opius.ai

## Submission Requirements
1. Extension manifest with Opius AI branding
2. Screenshots and demo videos
3. Documentation and user guides
4. Security compliance verification
```

### **PyPI (Python Package Index)**
```markdown
# PyPI Account Setup

## Account Creation
1. Go to: https://pypi.org/account/register/
2. Username: opius-ai
3. Email: pypi@opius.ai
4. Verify email

## Package Information
- **Package Name**: opius-planner
- **Author**: Opius AI
- **Maintainer Email**: support@opius.ai
- **Homepage**: https://opius.ai/planner
- **Repository**: https://github.com/opius-ai/planner-agent
```

### **npm Registry**
```markdown
# npm Account Setup

## Account Creation
1. Go to: https://www.npmjs.com/signup
2. Username: opius-ai
3. Email: npm@opius.ai
4. Verify email

## Organization Setup
1. Create organization: @opius-ai
2. Package name: @opius-ai/planner
3. Billing: Add payment method for private packages (if needed)
```

### **Docker Hub**
```markdown
# Docker Hub Account Setup

## Account Creation
1. Go to: https://hub.docker.com/signup
2. Username: opius-ai
3. Email: docker@opius.ai
4. Verify email

## Organization Setup
1. Create organization: opius-ai
2. Repository name: planner
3. Full image: opius-ai/planner
```

### **JetBrains Plugin Repository**
```markdown
# JetBrains Marketplace Setup

## Account Creation
1. Go to: https://plugins.jetbrains.com/author/me
2. Sign up with opius.ai email
3. Complete developer profile

## Plugin Information
- **Plugin Name**: Opius Planner
- **Vendor**: Opius AI
- **Contact**: jetbrains@opius.ai
- **Website**: https://opius.ai/planner
```

### **Homebrew (macOS/Linux)**
```markdown
# Homebrew Formula Setup

## Requirements
1. **GitHub Account**: opius-ai
2. **Repository**: homebrew-tap
3. **Formula Name**: opius-planner

## Submission Process
1. Create formula file
2. Test installation locally
3. Submit PR to homebrew-core (for official inclusion)
4. Or maintain in homebrew-tap (custom tap)
```

### **Chocolatey (Windows)**
```markdown
# Chocolatey Package Setup

## Account Creation
1. Go to: https://chocolatey.org/account/register
2. Username: opius-ai
3. Email: chocolatey@opius.ai

## Package Information
- **Package ID**: opius-planner
- **Maintainer**: Opius AI
- **Project URL**: https://opius.ai/planner
- **Source**: https://github.com/opius-ai/planner-agent
```

### **Conda (Anaconda)**
```markdown
# Conda Package Setup

## Account Creation
1. Go to: https://anaconda.org/account/register
2. Username: opius-ai
3. Email: conda@opius.ai

## Package Information
- **Package Name**: opius-planner
- **Channel**: conda-forge (preferred) or opius-ai
- **Recipe Repository**: https://github.com/conda-forge/opius-planner-feedstock
```

## 🔑 **Required Secrets and Tokens**

Create these accounts and generate tokens for CI/CD:

```yaml
# GitHub Repository Secrets (Add to opius-ai/planner-agent repo)
VSCODE_MARKETPLACE_TOKEN: "Personal Access Token from Azure DevOps"
CURSOR_MARKETPLACE_TOKEN: "Token from Cursor team"  
WINDSURF_MARKETPLACE_TOKEN: "Token from Windsurf team"
JETBRAINS_TOKEN: "JetBrains Hub token"
PYPI_API_TOKEN: "PyPI API token"
NPM_TOKEN: "npm automation token"
DOCKER_HUB_TOKEN: "Docker Hub access token"
HOMEBREW_GITHUB_TOKEN: "GitHub token for Homebrew formula"
CHOCOLATEY_API_KEY: "Chocolatey API key"
CONDA_TOKEN: "Anaconda cloud token"

# Code Signing Certificates
APPLE_DEVELOPER_ID: "Apple Developer certificate"
WINDOWS_CERT: "Windows code signing certificate"
```

## 📋 **Token Generation Steps**

### **VS Code Marketplace Token**
1. Go to: https://dev.azure.com/opius-ai
2. User Settings → Personal Access Tokens
3. Create new token with "Marketplace (publish)" scope
4. Copy token and add to GitHub secrets as `VSCODE_MARKETPLACE_TOKEN`

### **PyPI API Token**
1. Log into PyPI account
2. Account settings → API tokens
3. Create token with "Entire account" scope (or specific project)
4. Copy token and add to GitHub secrets as `PYPI_API_TOKEN`

### **npm Token**
1. Log into npm account
2. Access tokens → Generate new token
3. Select "Automation" type
4. Copy token and add to GitHub secrets as `NPM_TOKEN`

### **Docker Hub Token**
1. Log into Docker Hub
2. Account Settings → Security → Access Tokens
3. Create new access token
4. Copy token and add to GitHub secrets as `DOCKER_HUB_TOKEN`

### **GitHub Token (for Homebrew)**
1. GitHub Settings → Developer settings → Personal access tokens
2. Generate token with "public_repo" scope
3. Copy token and add to GitHub secrets as `HOMEBREW_GITHUB_TOKEN`

## 🛡️ **Security Best Practices**

### **Token Management**
- **Rotate tokens** every 90 days
- **Use minimal scopes** for each token
- **Monitor token usage** in platform dashboards
- **Revoke immediately** if compromised
- **Store in GitHub secrets** only, never in code

### **Account Security**
- **Enable 2FA** on all marketplace accounts
- **Use strong, unique passwords**
- **Monitor login activity** regularly
- **Set up email alerts** for account changes
- **Maintain backup access** methods

### **Code Signing**
- **Apple Developer Certificate**: Required for macOS notarization
- **Windows Code Signing**: Required for Windows trust
- **Store certificates** in secure CI/CD secrets
- **Renew certificates** before expiration
- **Test signing process** in CI/CD pipeline

## 🔄 **Maintenance Checklist**

### **Monthly Tasks**
- [ ] Check token expiration dates
- [ ] Review download metrics from all platforms
- [ ] Update package descriptions if needed
- [ ] Monitor user feedback and reviews

### **Quarterly Tasks**
- [ ] Rotate authentication tokens
- [ ] Update company information across platforms
- [ ] Review and update privacy policies
- [ ] Audit access permissions

### **Annual Tasks**
- [ ] Renew code signing certificates
- [ ] Review and update terms of service
- [ ] Conduct security audit of all accounts
- [ ] Update branding assets if needed

## 📞 **Support Contacts**

### **Marketplace Support**
- **VS Code**: https://aka.ms/vscode-publish-help
- **JetBrains**: https://plugins.jetbrains.com/docs/marketplace
- **PyPI**: https://pypi.org/help/
- **npm**: https://www.npmjs.com/support
- **Docker Hub**: https://hub.docker.com/support/contact

### **Emergency Contacts**
- **Security Issues**: security@opius.ai
- **Marketplace Issues**: marketplace@opius.ai
- **General Support**: support@opius.ai
- **Technical Issues**: tech@opius.ai
