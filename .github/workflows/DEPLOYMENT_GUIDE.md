# Deployment Pipelines Guide

This document explains the deployment pipeline setup for the Draw.io to Jira/Confluence Processor project.

## Overview

We have implemented a two-workflow deployment system:

1. **PR Deployment Workflow** (`pr-deploy.yml`)
   - Triggered when a Pull Request is opened, synchronized, or reopened
   - Provides manual deployment to Dev environment for testing PR changes

2. **Main Branch Deployment Workflow** (`main-deploy.yml`)
   - Triggered automatically when code is merged to the `main` branch
   - Sequential deployment pipeline: Dev → QA → Prod
   - Dev deployment is automatic
   - QA and Prod deployments require manual approval

## Workflow Details

### PR Deployment Workflow

**Trigger:** Pull Request events (opened, synchronize, reopened)

**Jobs:**
- `deploy-dev` (Manual approval required)
  - Checks out the PR code
  - Sets up Python 3.10
  - Installs dependencies
  - Runs tests
  - Deploys to Dev environment

**Use Case:** Test changes in Dev environment before merging to main

### Main Branch Deployment Workflow

**Trigger:** Push to `main` branch

**Jobs:**

1. **deploy-dev** (Automatic)
   - Runs immediately after merge to main
   - Checks out code
   - Sets up Python 3.10
   - Installs dependencies
   - Runs tests
   - Deploys to Dev environment

2. **deploy-qa** (Manual approval required)
   - Runs after `deploy-dev` completes successfully
   - Requires manual approval via GitHub environment protection rules
   - Deploys to QA environment

3. **deploy-prod** (Manual approval required)
   - Runs after `deploy-qa` completes successfully
   - Requires manual approval via GitHub environment protection rules
   - Deploys to Production environment

## Setting Up GitHub Environments

To enable manual approvals for QA and Prod deployments, you need to configure GitHub Environments:

### Step 1: Create Environments

1. Go to your GitHub repository
2. Click on **Settings** → **Environments**
3. Create three environments:
   - `dev`
   - `qa`
   - `prod`

### Step 2: Configure Environment Protection Rules

For the **dev** environment (for PR workflow):
1. Click on the `dev` environment
2. Check **Required reviewers**
3. Add team members who can approve Dev deployments for PRs
4. Save protection rules

For the **qa** environment:
1. Click on the `qa` environment
2. Check **Required reviewers**
3. Add team members who can approve QA deployments
4. Optionally, add a **Wait timer** (e.g., 5 minutes) for additional safety
5. Save protection rules

For the **prod** environment:
1. Click on the `prod` environment
2. Check **Required reviewers**
3. Add senior team members who can approve Production deployments
4. **Recommended:** Add multiple reviewers and require at least 2 approvals
5. Optionally, add a **Wait timer** (e.g., 10 minutes) for additional safety
6. Consider limiting to protected branches only
7. Save protection rules

### Step 3: Configure Environment Secrets (Optional)

If your deployments require secrets (API keys, credentials, etc.):

1. Go to each environment in **Settings** → **Environments**
2. Click **Add secret** under Environment secrets
3. Add deployment-specific secrets:
   - `DEV_SERVER_URL`
   - `QA_SERVER_URL`
   - `PROD_SERVER_URL`
   - `DEPLOY_TOKEN`
   - etc.

## Deployment Flow

### For Pull Requests:

1. Developer creates a PR
2. PR workflow triggers automatically
3. `deploy-dev` job appears and waits for manual approval
4. Reviewer approves the deployment
5. Code is deployed to Dev environment for testing
6. Once tested and approved, PR is merged to main

### For Main Branch (After Merge):

1. Code is merged to `main` branch
2. `deploy-dev` job runs automatically
3. Once Dev deployment succeeds, `deploy-qa` job appears and waits for approval
4. QA team approves deployment
5. Code is deployed to QA environment
6. Once QA testing is complete, `deploy-prod` job waits for approval
7. Production team approves deployment
8. Code is deployed to Production environment

## Customizing Deployments

### Adding Actual Deployment Commands

Currently, the workflows contain placeholder deployment commands. Update them based on your deployment strategy:

#### Example: Docker Deployment

```yaml
- name: Deploy to Dev Environment
  run: |
    echo "Building Docker image..."
    docker build -t myapp:${{ github.sha }} .
    docker tag myapp:${{ github.sha }} myapp:latest
    
    echo "Pushing to registry..."
    docker push myapp:${{ github.sha }}
    docker push myapp:latest
    
    echo "Deploying to Dev server..."
    ssh user@dev-server "docker pull myapp:latest && docker-compose up -d"
```

#### Example: SSH/SCP Deployment

```yaml
- name: Deploy to QA Environment
  run: |
    echo "Copying files to QA server..."
    scp -r ./drawio-jira-confluence/* user@qa-server:/var/www/app/
    
    echo "Restarting application..."
    ssh user@qa-server "cd /var/www/app && systemctl restart myapp"
```

#### Example: Cloud Deployment (AWS, Azure, GCP)

```yaml
- name: Deploy to Prod Environment
  run: |
    echo "Deploying to AWS..."
    aws s3 sync ./frontend s3://my-bucket/
    aws cloudfront create-invalidation --distribution-id DISTID --paths "/*"
```

### Adding Tests

Update the test sections with your actual test commands:

```yaml
- name: Run tests
  run: |
    cd drawio-jira-confluence/backend
    pytest tests/ --cov=. --cov-report=xml
    
    # Or for frontend tests
    cd ../frontend
    npm test
```

### Adding Build Steps

If you need to build your application:

```yaml
- name: Build application
  run: |
    cd drawio-jira-confluence/backend
    python setup.py build
    
    # Or for frontend
    cd ../frontend
    npm run build
```

## Monitoring Deployments

### Viewing Workflow Runs

1. Go to **Actions** tab in your repository
2. Select the workflow (PR Deployment or Main Branch Deployment)
3. View the status of each job
4. Click on a job to see detailed logs

### Approving Deployments

1. When a deployment requires approval, you'll see a yellow waiting status
2. Click on the workflow run
3. Click **Review deployments**
4. Select the environment(s) to approve
5. Add a comment (optional)
6. Click **Approve and deploy**

### Deployment Notifications

GitHub will send notifications:
- When a deployment is waiting for approval
- When a deployment succeeds or fails
- To users who need to approve deployments

## Security Best Practices

1. **Use Environment Secrets:** Store all sensitive data in GitHub environment secrets
2. **Limit Approvers:** Only add trusted team members as required reviewers
3. **Branch Protection:** Enable branch protection rules on `main` branch
4. **Audit Logs:** Regularly review deployment logs and approvals
5. **Least Privilege:** Give workflows only the permissions they need

## Troubleshooting

### Workflow Not Triggering

- Check that the workflow file is in `.github/workflows/`
- Verify the syntax is valid YAML
- Ensure you have push permissions to the repository

### Deployment Failing

- Check the workflow logs for error messages
- Verify all required secrets are configured
- Test deployment commands locally first

### Approval Not Working

- Ensure environments are configured in repository settings
- Verify required reviewers are added to the environment
- Check that reviewers have appropriate permissions

## Next Steps

1. **Customize deployment commands** based on your infrastructure
2. **Add comprehensive tests** to validate deployments
3. **Set up monitoring** for your deployed environments
4. **Configure notifications** for deployment status
5. **Document rollback procedures** for production

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Environments Documentation](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

---

**Happy Deploying! 🚀**
