#!/usr/bin/env python3
"""
Setup script to create the complete project structure
Run this script to generate all necessary files and folders
"""

import os
import shutil
import sys

# Handle Unicode encoding issues on Windows
def safe_print(text):
    """Print text with fallback for encoding issues"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Fallback to ASCII-safe version
        print(text.encode('ascii', 'replace').decode('ascii'))

def create_directory_structure():
    """Create the project directory structure"""
    
    print("🚀 Creating Draw.io to Jira/Confluence Processor Project...")
    print()
    
    # Define directory structure
    directories = [
        'drawio-jira-confluence',
        'drawio-jira-confluence/backend',
        'drawio-jira-confluence/frontend',
        'drawio-jira-confluence/examples',
        'drawio-jira-confluence/docs',
    ]
    
    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    print()
    
    # Create backend/requirements.txt
    print("📦 Creating backend/requirements.txt...")
    with open('drawio-jira-confluence/backend/requirements.txt', 'w', encoding='utf-8') as f:
        f.write("""flask==3.0.0
flask-cors==4.0.0
requests==2.31.0
""")
    
    # Create backend/README.md
    print("📝 Creating backend/README.md...")
    with open('drawio-jira-confluence/backend/README.md', 'w', encoding='utf-8') as f:
        f.write("""# Backend API

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
# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Server runs on port 5000 by default.

## Configuration

The API expects configuration in the request body with:
- Jira URL
- Confluence URL
- Email
- API Token

Get your API token from: https://id.atlassian.com/manage-profile/security/api-tokens
""")
    
    # Create frontend/README.md
    print("📝 Creating frontend/README.md...")
    with open('drawio-jira-confluence/frontend/README.md', 'w', encoding='utf-8') as f:
        f.write("""# Frontend UI

Web-based interface for the Draw.io to Jira/Confluence processor.

## Features

- 🎨 Drag & drop file upload
- 📦 Batch processing
- 📄 Template management
- 📊 Real-time progress tracking
- 📥 CSV export
- 💾 Local configuration storage

## Usage

### Option 1: Direct Browser Access
Simply open `index.html` in any modern web browser.

### Option 2: Local HTTP Server (Recommended)
```bash
# Using Python 3
python -m http.server 8000

# Using Node.js (if installed)
npx http-server -p 8000
```

Then navigate to `http://localhost:8000`

## Configuration

1. Go to the **Configuration** tab
2. Enter your Atlassian credentials
3. Set default project and space keys
4. Save configuration (stored in browser localStorage)

## Supported File Types

- Draw.io: `.drawio`, `.xml`
- Mermaid: `.mmd`, `.txt`

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
""")
    
    # Create .gitignore
    print("🔒 Creating .gitignore...")
    with open('drawio-jira-confluence/.gitignore', 'w', encoding='utf-8') as f:
        f.write("""# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo
*.sublime-*

# OS
.DS_Store
Thumbs.db
desktop.ini

# Uploads
uploads/
temp/

# Config
config.json
.env
*.local

# Logs
*.log
logs/

# Test files
test_*.drawio
test_*.xml
test_*.mmd
""")
    
    # Create LICENSE
    print("📜 Creating LICENSE...")
    with open('drawio-jira-confluence/LICENSE', 'w', encoding='utf-8') as f:
        f.write("""MIT License

Copyright (c) 2024 Draw.io to Jira/Confluence Processor

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
""")
    
    # Create main README.md
    print("📚 Creating main README.md...")
    with open('drawio-jira-confluence/README.md', 'w', encoding='utf-8') as f:
        f.write("""# 🎨 Draw.io to Jira/Confluence Processor

Automatically convert your draw.io diagrams into Jira tickets and Confluence documentation with generated Mermaid sequence diagrams.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## ✨ Features

- 📊 **Draw.io Processing** - Parse and extract diagram information
- 🔷 **Mermaid Generation** - Auto-generate sequence diagrams
- 🎫 **Jira Integration** - Create tickets automatically
- 📄 **Confluence Pages** - Generate documentation pages
- 📦 **Batch Processing** - Process multiple files at once
- 🎨 **Drag & Drop UI** - Modern, intuitive interface
- 📤 **Export Results** - Download processing results as CSV
- 📝 **Multiple Templates** - Choose from pre-built templates

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Modern web browser
- Atlassian account with API access

### Installation

1. **Clone or download this project**

2. **Install backend dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

3. **Start the backend server:**
```bash
python app.py
```

4. **Open the frontend:**
```bash
cd ../frontend
# Open index.html in your browser
# OR use a local server:
python -m http.server 8000
```

5. **Configure your settings:**
   - Open the web interface
   - Go to Configuration tab
   - Add your Atlassian credentials
   - Save configuration

## 📖 Usage

### Process Single File

1. Go to **Process Draw.io** tab
2. Drag & drop your .drawio file
3. Set project and space keys
4. Click **Process**
5. Get links to created Jira ticket and Confluence page

### Batch Processing

1. Go to **Batch Process** tab
2. Drop multiple .drawio files
3. Configure settings
4. Click **Process All Files**
5. Export results to CSV

### Mermaid Diagrams

1. Go to **Process Mermaid** tab
2. Paste or upload Mermaid code
3. Set project details
4. Process to create ticket and page

## 🏗️ Project Structure

```
drawio-jira-confluence/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── requirements.txt       # Python dependencies
│   └── README.md
├── frontend/
│   ├── index.html            # Web UI
│   └── README.md
├── examples/                  # Sample files
├── docs/                      # Documentation
├── .gitignore
├── LICENSE
└── README.md
```

## 🔧 Configuration

### Atlassian API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Create a new API token
3. Save it securely (you won't see it again)
4. Use it in the Configuration tab

### Environment Variables (Optional)

Create `.env` file in backend directory:
```env
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

## 📚 API Documentation

### Health Check
```bash
GET /api/health
```

### Process Draw.io
```bash
POST /api/process-drawio
Content-Type: multipart/form-data

Form Data:
- file: Draw.io file
- config: JSON configuration
- projectKey: Jira project
- spaceKey: Confluence space
- issueType: Issue type
- template: Template name
```

### Batch Process
```bash
POST /api/batch-process
Content-Type: multipart/form-data

Form Data:
- files[]: Multiple files
- config: JSON configuration
- projectKey, spaceKey, etc.
```

See [API.md](docs/API.md) for complete documentation.

## 🎨 Templates

Three built-in templates:
- **Simple** - Basic layout with diagram
- **Technical** - Detailed technical docs
- **Detailed** - Comprehensive with all sections

## 🐛 Troubleshooting

### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### CORS Errors
- Ensure backend is running on port 5000
- Check API URL in Configuration tab
- Verify flask-cors is installed

### API Authentication Errors
- Verify API token is correct
- Check email matches Atlassian account
- Ensure you have project permissions

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for more help.

## 🔒 Security

- Never commit API tokens
- Use environment variables for secrets
- Enable HTTPS in production
- Implement rate limiting
- Validate all inputs

## 🚢 Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```bash
docker build -t drawio-processor .
docker run -p 5000:5000 drawio-processor
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- Atlassian for Jira & Confluence APIs
- Flask web framework
- Mermaid diagram library
- Draw.io for diagram creation

## 📞 Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](issues/)
- 💬 [Discussions](discussions/)

---

Made with ❤️ for better documentation workflows
""")
    
    # Create example files
    print("📋 Creating example files...")
    
    # Sample Mermaid diagram
    with open('drawio-jira-confluence/examples/sample_mermaid.mmd', 'w', encoding='utf-8') as f:
        f.write("""sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Database
    
    User->>Frontend: Open application
    Frontend->>API: Request data
    API->>Database: Query records
    Database-->>API: Return results
    API-->>Frontend: Send response
    Frontend-->>User: Display data
""")
    
    # Sample draw.io (basic XML structure)
    with open('drawio-jira-confluence/examples/sample_diagram.drawio', 'w', encoding='utf-8') as f:
        f.write("""<mxfile host="app.diagrams.net" modified="2024-01-01T00:00:00.000Z">
  <diagram name="Sample System" id="sample">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="2" value="User" style="shape=umlActor;verticalLabelPosition=bottom;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="30" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="3" value="System" style="rounded=1;" vertex="1" parent="1">
          <mxGeometry x="120" y="40" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="4" value="" style="endArrow=classic;" edge="1" parent="1" source="2" target="3">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
""")
    
    # Create documentation files
    print("📖 Creating documentation...")
    
    with open('drawio-jira-confluence/docs/SETUP.md', 'w', encoding='utf-8') as f:
        f.write("""# Setup Guide

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
venv\\Scripts\\activate
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
""")
    
    with open('drawio-jira-confluence/docs/TROUBLESHOOTING.md', 'w', encoding='utf-8') as f:
        f.write("""# Troubleshooting Guide

Common issues and solutions.

## Backend Issues

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port 5000
# Windows:
netstat -ano | findstr :5000

# macOS/Linux:
lsof -i :5000

# Kill the process or change port in app.py
```

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Ensure virtual environment is activated
# Then reinstall:
pip install -r requirements.txt
```

### CORS Errors

**Error:** Browser console shows CORS errors

**Solution:**
1. Verify backend is running
2. Check `flask-cors` is installed:
```bash
pip install flask-cors
```
3. Restart backend server

## Frontend Issues

### Configuration Not Saving

**Issue:** Settings don't persist after refresh

**Solution:**
- Check browser localStorage is enabled
- Try a different browser
- Check browser console for errors

### Files Won't Upload

**Issue:** Drag & drop doesn't work

**Solution:**
1. Check file type (.drawio, .xml, .mmd, .txt only)
2. Check file size (max 16MB by default)
3. Try clicking instead of dragging
4. Check browser console for errors

## API Issues

### 401 Unauthorized

**Error:** Authentication failed

**Solution:**
1. Verify API token is correct
2. Check email matches Atlassian account
3. Generate new API token if needed
4. Ensure no extra spaces in credentials

### 403 Forbidden

**Error:** Permission denied

**Solution:**
1. Verify you have permissions in project
2. Check project key is correct
3. Verify space key exists
4. Check you can create issues/pages manually

### 404 Not Found

**Error:** Resource not found

**Solution:**
1. Check Jira/Confluence URLs are correct
2. Remove trailing slashes (except for /wiki)
3. Verify project and space exist
4. Test URLs in browser

### 400 Bad Request

**Error:** Invalid request

**Solution:**
1. Check all required fields are filled
2. Verify file format is correct
3. Check configuration JSON is valid
4. Review backend logs for details

## File Processing Issues

### Draw.io Parse Error

**Error:** Invalid draw.io file format

**Solution:**
1. Verify file is valid draw.io XML
2. Try opening in draw.io to check
3. Re-export from draw.io
4. Check file isn't corrupted

### Mermaid Syntax Error

**Error:** Invalid Mermaid syntax

**Solution:**
1. Validate syntax at https://mermaid.live
2. Check for typos in participant names
3. Ensure proper arrow syntax (->>, -->>)
4. Review Mermaid documentation

## Batch Processing Issues

### Some Files Fail

**Issue:** Batch processing completes but some files failed

**Solution:**
1. Check error messages for each file
2. Process failed files individually to see details
3. Verify all files are valid format
4. Check file names don't have special characters

### Progress Bar Stuck

**Issue:** Progress bar doesn't update

**Solution:**
1. Check browser console for errors
2. Refresh page and try again
3. Try smaller batch sizes
4. Check network connection

## Performance Issues

### Slow Processing

**Issue:** Files take long to process

**Solution:**
1. Process fewer files at once
2. Check network connection
3. Verify Atlassian services are responsive
4. Check backend server resources

### Memory Errors

**Error:** Out of memory

**Solution:**
1. Reduce batch size
2. Process files individually
3. Restart backend server
4. Check file sizes

## Getting Help

If your issue isn't listed:

1. Check backend logs:
```bash
# Backend prints detailed errors
python app.py
```

2. Check browser console:
   - F12 to open developer tools
   - Look at Console tab
   - Look at Network tab for API calls

3. Test with sample files:
   - Use files from `examples/` directory
   - If samples work, issue is with your files

4. Verify configuration:
   - Test API token with curl:
```bash
curl -u email@example.com:API_TOKEN \\
  https://your-domain.atlassian.net/rest/api/3/myself
```

## Still Need Help?

- Create detailed issue with:
  - Error message
  - Steps to reproduce
  - Browser/Python versions
  - Configuration (without sensitive data!)
  - Backend logs
""")
    
    print()
    print("✅ Project structure created successfully!")
    print()
    print("📋 Next steps:")
    print("1. Copy app.py to: drawio-jira-confluence/backend/")
    print("2. Copy index.html to: drawio-jira-confluence/frontend/")
    print("3. Navigate to backend folder: cd drawio-jira-confluence/backend")
    print("4. Install dependencies: pip install -r requirements.txt")
    print("5. Run the server: python app.py")
    print("6. Open frontend/index.html in your browser")
    print()
    print("🎉 Happy processing!")

if __name__ == '__main__':
    create_directory_structure()