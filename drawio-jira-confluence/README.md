# 🎨 Draw.io to Jira/Confluence Processor

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
