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
