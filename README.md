# Draw.io to Jira/Confluence Processor - Complete Project

## 📦 Project Structure

```
drawio-jira-confluence/
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── requirements.txt          # Python dependencies
│   └── README.md                 # Backend documentation
├── frontend/
│   ├── index.html                # Main UI application
│   └── README.md                 # Frontend documentation
├── examples/
│   ├── sample_diagram.drawio     # Sample draw.io file
│   └── sample_mermaid.mmd        # Sample Mermaid file
├── docs/
│   ├── SETUP.md                  # Detailed setup guide
│   ├── API.md                    # API documentation
│   └── TROUBLESHOOTING.md        # Common issues and solutions
├── .gitignore
├── LICENSE
└── README.md                     # Main project documentation
```

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A modern web browser (Chrome, Firefox, Safari, or Edge)
- Atlassian account with API access

### Step 1: Download the Project

You can download all the files individually or create them as shown below:

### Step 2: Set Up the Backend

1. **Navigate to the backend directory:**
```bash
cd drawio-jira-confluence/backend
```

2. **Create a virtual environment (recommended):**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the Flask server:**
```bash
python app.py
```

The server will start on `http://localhost:5000`

### Step 3: Open the Frontend

1. **Navigate to the frontend directory:**
```bash
cd ../frontend
```

2. **Open index.html in your browser:**
   - **Option 1**: Double-click `index.html`
   - **Option 2**: Use a local server (recommended):
     ```bash
     # Python 3
     python -m http.server 8000
     
     # Then open: http://localhost:8000
     ```

### Step 4: Configure Your Atlassian Settings

1. Get your API token from: https://id.atlassian.com/manage-profile/security/api-tokens
2. In the UI, go to the **Configuration** tab
3. Fill in:
   - Jira URL (e.g., `https://your-domain.atlassian.net`)
   - Confluence URL (e.g., `https://your-domain.atlassian.net/wiki`)
   - Your email
   - API token
   - Default project key and space key
4. Click **Save Configuration**

### Step 5: Start Processing!

You can now:
- Upload draw.io files
- Process Mermaid diagrams
- Batch process multiple files
- Export results to CSV

## 📄 File Contents

### backend/requirements.txt
```
flask==3.0.0
flask-cors==4.0.0
requests==2.31.0
```

### backend/README.md
```markdown
# Backend API

Flask-based REST API for processing draw.io and Mermaid diagrams.

## Endpoints

- `GET /api/health` - Health check
- `GET /api/templates` - List available templates
- `GET /api/template/<name>` - Get specific template
- `POST /api/process-drawio` - Process single draw.io file
- `POST /api/process-mermaid` - Process Mermaid diagram
- `POST /api/batch-process` - Process multiple files
- `POST /api/export-results` - Export results to CSV

## Running

```bash
python app.py
```

Server runs on port 5000 by default.
```

### frontend/README.md
```markdown
# Frontend UI

Web-based interface for the Draw.io to Jira/Confluence processor.

## Features

- Drag & drop file upload
- Batch processing
- Template management
- Real-time progress tracking
- CSV export

## Usage

Open `index.html` in any modern web browser. For best results, serve it with a local HTTP server:

```bash
python -m http.server 8000
```

Then navigate to `http://localhost:8000`
```

### .gitignore
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Uploads
uploads/
*.drawio
*.xml
*.mmd

# Config
config.json
.env

# Logs
*.log
```

### LICENSE
```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file in the backend directory:

```env
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

### API Configuration

The frontend automatically uses `http://localhost:5000` as the API URL. You can change this in the Configuration tab.

## 📚 API Documentation

### Process Draw.io File

```bash
POST /api/process-drawio
Content-Type: multipart/form-data

Parameters:
- file: Draw.io file (.drawio or .xml)
- config: JSON string with Atlassian credentials
- projectKey: Jira project key
- spaceKey: Confluence space key
- issueType: Type of Jira issue (Task, Story, etc.)
- priority: Priority level (optional)
- template: Template name (simple, technical, detailed)
- parentPageId: Parent page ID (optional)

Response:
{
  "success": true,
  "jiraTicket": {
    "key": "PROJ-123",
    "id": "10001",
    "url": "https://..."
  },
  "confluencePage": {
    "id": "12345",
    "url": "https://..."
  },
  "mermaidDiagram": "sequenceDiagram..."
}
```

### Batch Process

```bash
POST /api/batch-process
Content-Type: multipart/form-data

Parameters:
- files[]: Multiple draw.io files
- config: JSON string with Atlassian credentials
- projectKey: Jira project key
- spaceKey: Confluence space key
- issueType: Type of Jira issue
- template: Template name

Response:
{
  "success": true,
  "processed": 5,
  "failed": 0,
  "results": [...],
  "errors": [...]
}
```

## 🐛 Troubleshooting

### Backend Won't Start

1. **Check Python version:**
   ```bash
   python --version  # Should be 3.8+
   ```

2. **Reinstall dependencies:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Check port availability:**
   ```bash
   # On Windows
   netstat -ano | findstr :5000
   
   # On macOS/Linux
   lsof -i :5000
   ```

### CORS Errors

If you see CORS errors in the browser console:

1. Make sure the Flask server is running
2. Check that `flask-cors` is installed
3. Verify the API URL in Configuration matches your backend URL

### Jira/Confluence API Errors

1. **401 Unauthorized:**
   - Check your API token is correct
   - Verify your email is correct
   - Ensure the token hasn't expired

2. **403 Forbidden:**
   - Check you have permissions in the project/space
   - Verify the project key and space key exist

3. **404 Not Found:**
   - Double-check the Jira/Confluence URLs
   - Ensure URLs don't have trailing slashes (except Confluence wiki URL)

### File Upload Issues

1. **File too large:**
   - Maximum file size is 16MB by default
   - Modify `MAX_CONTENT_LENGTH` in `app.py` to increase

2. **Invalid file type:**
   - Only .drawio, .xml, .mmd, and .txt files are accepted
   - Check the file extension is correct

## 🔒 Security Best Practices

1. **Never commit API tokens** to version control
2. **Use environment variables** for sensitive data
3. **Enable HTTPS** in production
4. **Implement rate limiting** for API endpoints
5. **Validate all user inputs** on the backend
6. **Use secure token storage** (consider encryption)

## 📈 Production Deployment

### Backend (Flask)

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend

Host the `index.html` file on any static hosting service:
- GitHub Pages
- Netlify
- Vercel
- AWS S3 + CloudFront
- Azure Static Web Apps

### Docker Deployment (Optional)

Create a `Dockerfile` for the backend:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t drawio-processor .
docker run -p 5000:5000 drawio-processor
```

## 🚀 Deployment Pipeline

This project includes automated deployment pipelines for Dev, QA, and Production environments.

### Pipeline Overview

**For Pull Requests:**
- Manual deployment to **Dev** environment available for testing PR changes
- Requires approval before deployment

**For Main Branch (after merge):**
- **Dev**: Automatically deployed when code is merged to main
- **QA**: Manual approval required after Dev deployment succeeds
- **Prod**: Manual approval required after QA deployment succeeds

### Setup Instructions

1. Configure GitHub Environments in repository Settings → Environments
2. Create three environments: `dev`, `qa`, `prod`
3. Add required reviewers for manual approval gates
4. Configure environment-specific secrets if needed

For detailed setup and usage instructions, see [.github/workflows/DEPLOYMENT_GUIDE.md](.github/workflows/DEPLOYMENT_GUIDE.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation in `/docs`
- Review the troubleshooting guide

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎉 Acknowledgments

- Atlassian for Jira and Confluence APIs
- Flask framework
- Mermaid diagram library
- Draw.io for diagram creation

---

**Happy Processing! 🚀**