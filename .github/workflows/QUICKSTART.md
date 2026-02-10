# Deployment Pipeline Quick Reference

## 🎯 Quick Overview

This project uses GitHub Actions for automated deployments across three environments:

### Workflows

1. **PR Deployment** (`.github/workflows/pr-deploy.yml`)
   - Trigger: Pull Request opened/updated
   - Environment: Dev (manual approval)
   - Purpose: Test changes before merging

2. **Main Branch Deployment** (`.github/workflows/main-deploy.yml`)
   - Trigger: Push to main branch
   - Environments: Dev → QA → Prod
   - Flow: Automatic → Manual → Manual

## 📋 Deployment Flow

### Pull Request Workflow
```
PR Created → Deploy to Dev (Manual Approval) → Testing → Merge
```

### Main Branch Workflow
```
Merge to Main → Deploy to Dev (Automatic) → Deploy to QA (Manual) → Deploy to Prod (Manual)
```

## ⚙️ Environment Configuration Required

Before using the pipelines, configure these in GitHub:

1. **Go to**: Repository Settings → Environments
2. **Create**: Three environments (`dev`, `qa`, `prod`)
3. **Configure**: Required reviewers for each environment
4. **Add**: Environment-specific secrets (if needed)

### Recommended Protection Rules

| Environment | Required Reviewers | Wait Timer | Notes |
|-------------|-------------------|------------|-------|
| dev | 1 | None | Quick testing |
| qa | 1-2 | 5 min | QA validation |
| prod | 2+ | 10 min | Production safety |

## 🔑 Key Features

✅ **Automatic Dev deployment** on main branch merge  
✅ **Manual approvals** for QA and Prod  
✅ **Sequential pipeline** ensures proper testing flow  
✅ **PR preview** deployments for early testing  
✅ **Python dependency** installation included  
✅ **Deployment logs** for audit trail  

## 🛠️ Customization Points

The workflows include placeholder commands for:
- Running tests
- Building application
- Deploying to servers

Update these sections with your actual deployment commands:

```yaml
- name: Deploy to [Environment]
  run: |
    # Add your deployment commands here
    # Examples:
    # - docker build and push
    # - scp/rsync files
    # - kubectl apply
    # - terraform apply
    # - cloud provider CLI commands
```

## 📊 Monitoring Deployments

1. Go to **Actions** tab in repository
2. Select workflow run to view progress
3. Click **Review deployments** to approve when ready
4. Check logs for deployment status

## 🆘 Common Actions

### Approve a Deployment
1. Navigate to Actions → Select workflow run
2. Click "Review deployments"
3. Select environment(s) to approve
4. Add comment (optional)
5. Click "Approve and deploy"

### Cancel a Deployment
1. Navigate to Actions → Select workflow run
2. Click "Cancel workflow"

### Re-run a Failed Deployment
1. Navigate to Actions → Select failed workflow run
2. Click "Re-run all jobs" or "Re-run failed jobs"

## 📚 Full Documentation

For complete setup instructions, troubleshooting, and customization options, see:
- [DEPLOYMENT_GUIDE.md](.github/workflows/DEPLOYMENT_GUIDE.md)

## 🔒 Security Notes

- Never commit secrets to the repository
- Use GitHub Secrets for sensitive data
- Configure branch protection on `main`
- Limit approvers to trusted team members
- Review deployment logs regularly

---

Need help? Check the full [Deployment Guide](DEPLOYMENT_GUIDE.md) or open an issue.
