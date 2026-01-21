# Setup Guide

Complete guide for setting up the Draw.io to Jira/Confluence Processor.

## System Requirements

- **Python**: 3.8 or higher
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, or Edge 90+
- **RAM**: Minimum 2GB available
- **Disk**: 100MB for installation

## Installation Steps

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Frontend Setup

No installation required! The frontend is a static HTML file.

```bash
cd frontend

# Option 1: Direct browser access
# Just open index.html

# Option 2: Local server (recommended)
python -m http.server 8000
# Then visit: http://localhost:8000
```

### 3. Atlassian Configuration

1. **Get API Token:**
   - Visit: https://id.atlassian.com/manage-profile/security/api-tokens
   - Click "Create API token"
   - Give it a name (e.g., "Draw.io Processor")
   - Copy the token (you won't see it again!)

2. **Find Your URLs:**
   - Jira: `https://YOUR-DOMAIN.atlassian.net`
   - Confluence: `https://YOUR-DOMAIN.atlassian.net/wiki`

3. **Find Project and Space Keys:**
   - Jira project key: Check project settings
   - Confluence space key: Check space settings

### 4. First Run

1. Start backend:
```bash
cd backend
python app.py
```

2. Open frontend in browser

3. Go to Configuration tab

4. Fill in all fields:
   - Jira URL
   - Confluence URL
   - Your email
   - API token
   - Project key
   - Space key

5. Click "Save Configuration"

6. Test with a sample file from `examples/`

## Verification

Test your setup:

1. **Backend Health Check:**
```bash
curl http://localhost:5000/api/health
```
Should return: `{"status": "healthy", "version": "1.0.0"}`

2. **Process Sample File:**
   - Use `examples/sample_diagram.drawio`
   - Upload in UI
   - Check if Jira ticket and Confluence page are created

## Next Steps

- Read [API.md](API.md) for API documentation
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) if issues arise
- Review templates in the Templates tab

## Advanced Configuration

### Custom Port

Backend (app.py):
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
```

Frontend: Update API URL in Configuration tab to match

### Environment Variables

Create `.env` file:
```env
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
MAX_CONTENT_LENGTH=16777216  # 16MB
```

### HTTPS Setup

For production, use a reverse proxy like Nginx:
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:5000;
    }
}
```
