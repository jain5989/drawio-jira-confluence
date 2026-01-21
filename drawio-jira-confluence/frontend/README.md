# Frontend UI

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
