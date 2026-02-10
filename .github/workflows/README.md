# GitHub Actions Workflows

This directory contains the automated deployment pipelines for the Draw.io to Jira/Confluence Processor project.

## 📁 Files Overview

### Workflow Files (YAML)
- **`pr-deploy.yml`** - Pull Request deployment workflow
- **`main-deploy.yml`** - Main branch deployment workflow

### Documentation
- **`QUICKSTART.md`** - Quick reference guide (start here!)
- **`DEPLOYMENT_GUIDE.md`** - Complete setup and usage guide
- **`ARCHITECTURE.md`** - Technical details and visual diagrams
- **`README.md`** - This file

## 🚀 Quick Start

1. **Read the Quick Start Guide**: [QUICKSTART.md](QUICKSTART.md)
2. **Configure Environments**: Create `dev`, `qa`, `prod` in GitHub Settings
3. **Set Required Reviewers**: Add approvers for each environment
4. **Start Using**: Workflows will trigger automatically on PR and main branch events

## 📋 Workflow Summary

### PR Workflow (`pr-deploy.yml`)
- **Trigger**: When PR is opened/updated
- **Purpose**: Test changes in Dev environment
- **Approval**: Manual (via GitHub environment protection)

### Main Branch Workflow (`main-deploy.yml`)
- **Trigger**: When code is merged to main
- **Stages**: 
  1. Deploy to Dev (Automatic)
  2. Deploy to QA (Manual approval required)
  3. Deploy to Prod (Manual approval required)
- **Flow**: Sequential - each stage waits for previous to complete

## 🔑 Key Features

✅ **Automatic Dev deployment** on main branch  
✅ **Manual approval gates** for QA and Prod  
✅ **Sequential pipeline** for safe promotions  
✅ **PR preview deployments** for early testing  
✅ **Python syntax validation** before deployment  
✅ **Secure token permissions** (least privilege)  
✅ **Comprehensive logging** for audit trail  

## 📚 Documentation

| Document | Description | Best For |
|----------|-------------|----------|
| [QUICKSTART.md](QUICKSTART.md) | Quick reference and common tasks | Daily usage |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Complete setup instructions | Initial setup |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Technical details and diagrams | Understanding internals |

## 🛠️ Customization

To customize these workflows for your infrastructure:

1. Update deployment commands in the workflow files
2. Add your test commands (when tests are available)
3. Configure environment-specific secrets in GitHub
4. Adjust approval requirements per environment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 🔒 Security

- All workflows use explicit `permissions: contents: read`
- Environment secrets for sensitive data
- Manual approvals for production deployments
- Python syntax validation before deployment
- No security vulnerabilities detected by CodeQL

## ✅ Status

- [x] PR deployment workflow created
- [x] Main branch deployment workflow created
- [x] Comprehensive documentation provided
- [x] Security best practices implemented
- [x] YAML syntax validated
- [x] CodeQL security scan passed

## 📞 Support

For questions or issues:
1. Check the [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
2. Review workflow logs in GitHub Actions tab
3. Open an issue in the repository

---

**Ready to deploy! 🚀**
