# Deployment Pipeline Architecture

## Visual Flow Diagram

### PR Workflow
```
┌─────────────────┐
│  Pull Request   │
│     Created     │
└────────┬────────┘
         │
         v
┌────────────────────┐
│  Deploy to Dev     │
│  (Manual Approval) │
└────────┬───────────┘
         │
         v
┌────────────────────┐
│   Test Changes     │
│   in Dev Env       │
└────────┬───────────┘
         │
         v
┌────────────────────┐
│   Review & Merge   │
│     to Main        │
└────────────────────┘
```

### Main Branch Workflow
```
┌──────────────────┐
│   Code Merged    │
│    to Main       │
└────────┬─────────┘
         │
         v
┌──────────────────┐
│  Deploy to Dev   │
│   (Automatic)    │
└────────┬─────────┘
         │
         v
┌──────────────────┐
│   Deploy to QA   │
│     (Manual)     │◄───── Requires Approval
└────────┬─────────┘
         │
         v
┌──────────────────┐
│  Deploy to Prod  │
│     (Manual)     │◄───── Requires Approval
└──────────────────┘
```

## Workflow Details

### PR Deployment Pipeline (`pr-deploy.yml`)

**Trigger:** Pull Request events
- `opened` - When a new PR is created
- `synchronize` - When new commits are pushed to the PR
- `reopened` - When a closed PR is reopened

**Jobs:**
1. **deploy-dev**
   - Environment: `dev`
   - Requires: Manual approval
   - Actions:
     - Checkout PR code
     - Setup Python 3.10
     - Install dependencies
     - Run tests
     - Deploy to Dev environment
     - Generate deployment summary

**Purpose:** Allow teams to test PR changes in a Dev environment before merging

### Main Branch Deployment Pipeline (`main-deploy.yml`)

**Trigger:** Push to `main` branch (typically after PR merge)

**Jobs:**

1. **deploy-dev** (Automatic)
   - Environment: `dev`
   - Requires: None (runs automatically)
   - Actions:
     - Checkout main branch code
     - Setup Python 3.10
     - Install dependencies
     - Run tests
     - Deploy to Dev environment
     - Generate deployment summary

2. **deploy-qa** (Manual)
   - Environment: `qa`
   - Requires: 
     - `deploy-dev` job completion
     - Manual approval from authorized reviewers
   - Actions:
     - Checkout main branch code
     - Setup Python 3.10
     - Install dependencies
     - Deploy to QA environment
     - Generate deployment summary

3. **deploy-prod** (Manual)
   - Environment: `prod`
   - Requires:
     - `deploy-qa` job completion
     - Manual approval from authorized reviewers
   - Actions:
     - Checkout main branch code
     - Setup Python 3.10
     - Install dependencies
     - Deploy to Production environment
     - Generate deployment summary

## Environment Configuration

### Required GitHub Settings

Each environment must be configured in: **Repository Settings → Environments**

#### Dev Environment
- **Protection Rules:** Optional for main branch, Required for PRs
- **Required Reviewers:** 1 team member
- **Deployment branches:** All branches (for PRs) or Protected branches only (for main)
- **Secrets:** Development environment secrets

#### QA Environment
- **Protection Rules:** Required reviewers
- **Required Reviewers:** 1-2 team members
- **Wait Timer:** Optional (5 minutes recommended)
- **Deployment branches:** Protected branches only
- **Secrets:** QA environment secrets

#### Prod Environment
- **Protection Rules:** Required reviewers + Wait timer
- **Required Reviewers:** 2+ senior team members
- **Wait Timer:** 10-15 minutes recommended
- **Deployment branches:** Protected branches only
- **Secrets:** Production environment secrets

## Deployment Dependencies

### Python Environment
- Python 3.10
- pip package manager
- Dependencies from `drawio-jira-confluence/backend/requirements.txt`

### GitHub Actions
- `actions/checkout@v4` - Code checkout
- `actions/setup-python@v5` - Python setup

## Security Considerations

### Branch Protection
- Require pull request reviews before merging
- Require status checks to pass
- Require conversation resolution before merging
- Enforce restrictions on who can push to main

### Environment Protection
- Use environment secrets for sensitive data
- Limit environment access to authorized teams
- Configure required reviewers for each environment
- Enable deployment protection rules

### Audit Trail
- All deployments are logged in GitHub Actions
- Approval history is tracked
- Deployment status is visible in the Actions tab
- Failed deployments can be reviewed and re-run

## Rollback Strategy

If a deployment fails or causes issues:

1. **Immediate Rollback:**
   - Revert the commit in main branch
   - Automatic Dev deployment will use previous code
   - Proceed with QA/Prod deployments as normal

2. **Manual Rollback:**
   - Use GitHub Actions to re-run a previous successful workflow
   - Deploy specific commit SHA to any environment

3. **Emergency Rollback:**
   - Deploy directly to affected environment using manual process
   - Document the incident and update workflows if needed

## Monitoring and Notifications

### Workflow Status
- Monitor in GitHub Actions tab
- View real-time logs for each job
- Receive notifications on failures

### Notifications
- Email notifications for:
  - Deployment waiting for approval
  - Deployment success/failure
  - Workflow run completion
- Configure in GitHub notification settings

### Slack Integration (Optional)
Add Slack notifications to workflows:
```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## Performance Considerations

### Job Execution Time
- **Dev Deployment:** ~2-3 minutes
- **QA Deployment:** ~2-3 minutes
- **Prod Deployment:** ~2-3 minutes

### Parallelization
- PR deployment runs independently
- Main branch deployments run sequentially
- Multiple PRs can deploy simultaneously

### Resource Usage
- Each job uses 1 runner
- Free tier: 2,000 minutes/month for private repos
- Public repos: Unlimited minutes

## Best Practices

1. **Test in Dev First:** Always validate changes in Dev before promoting
2. **Review Logs:** Check deployment logs before approving next stage
3. **Communicate:** Notify team before deploying to Prod
4. **Monitor:** Watch application metrics after deployment
5. **Document:** Keep deployment notes for audit trail
6. **Rollback Ready:** Have rollback plan before Prod deployment
7. **Off-Hours:** Consider deploying to Prod during low-traffic periods
8. **Gradual Rollout:** Use feature flags for risky changes

## Troubleshooting

### Workflow Not Starting
- Check workflow file syntax
- Verify trigger conditions are met
- Check repository permissions

### Deployment Failing
- Review job logs for errors
- Verify environment secrets are configured
- Test deployment commands locally

### Approval Not Working
- Verify required reviewers are configured
- Check reviewer has necessary permissions
- Ensure environment protection rules are set

### Timeout Issues
- Increase job timeout if needed
- Optimize deployment scripts
- Check network connectivity

---

For more information, see:
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Complete setup guide
- [QUICKSTART.md](QUICKSTART.md) - Quick reference guide
