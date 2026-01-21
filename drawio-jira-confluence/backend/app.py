"""
Flask Backend API for Draw.io to Jira/Confluence Integration
Features: File processing, batch operations, template management
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import xml.etree.ElementTree as ET
import base64
import urllib.parse
import requests
import json
from typing import Dict, List, Optional
import os
import tempfile
from werkzeug.utils import secure_filename
import zipfile
from io import BytesIO
import traceback

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'drawio', 'xml', 'mmd', 'txt'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class DrawioParser:
    """Parse draw.io XML files and extract diagram information"""
    
    def __init__(self, file_content: str):
        self.content = file_content
        self.tree = None
        
    def parse(self) -> Dict:
        """Parse the draw.io file and extract structured data"""
        try:
            self.tree = ET.fromstring(self.content)
        except ET.ParseError:
            # Try to decode if it's base64 encoded
            try:
                decoded = base64.b64decode(self.content)
                self.tree = ET.fromstring(decoded)
            except:
                raise ValueError("Invalid draw.io file format")
        
        diagram_data = {
            'title': self._extract_title(),
            'shapes': self._extract_shapes(),
            'connections': self._extract_connections(),
            'text_elements': self._extract_text_elements()
        }
        
        return diagram_data
    
    def _extract_title(self) -> str:
        """Extract diagram title"""
        diagram = self.tree.find('.//diagram')
        if diagram is not None and 'name' in diagram.attrib:
            return diagram.attrib['name']
        return "Untitled Diagram"
    
    def _extract_shapes(self) -> List[Dict]:
        """Extract all shapes from the diagram"""
        shapes = []
        for cell in self.tree.findall('.//mxCell'):
            if cell.get('vertex') == '1':
                shape = {
                    'id': cell.get('id'),
                    'value': self._decode_value(cell.get('value', '')),
                    'style': cell.get('style', '')
                }
                shapes.append(shape)
        return shapes
    
    def _extract_connections(self) -> List[Dict]:
        """Extract connections between shapes"""
        connections = []
        for cell in self.tree.findall('.//mxCell'):
            if cell.get('edge') == '1':
                connection = {
                    'id': cell.get('id'),
                    'source': cell.get('source'),
                    'target': cell.get('target'),
                    'value': self._decode_value(cell.get('value', ''))
                }
                connections.append(connection)
        return connections
    
    def _extract_text_elements(self) -> List[str]:
        """Extract all text elements from the diagram"""
        texts = []
        for cell in self.tree.findall('.//mxCell'):
            value = cell.get('value', '')
            if value:
                decoded = self._decode_value(value)
                texts.append(decoded)
        return texts
    
    def _decode_value(self, value: str) -> str:
        """Decode HTML entities and special characters"""
        if not value:
            return ""
        try:
            decoded = urllib.parse.unquote(value)
            # Remove HTML tags
            import re
            decoded = re.sub(r'<[^>]+>', '', decoded)
            return decoded.strip()
        except:
            return value


class MermaidGenerator:
    """Generate Mermaid sequence diagrams"""
    
    @staticmethod
    def generate_sequence_diagram(actors: List[str], interactions: List[Dict]) -> str:
        """Generate a Mermaid sequence diagram"""
        mermaid = "sequenceDiagram\n"
        
        for actor in actors:
            # Clean actor name for Mermaid
            clean_actor = actor.replace(' ', '_').replace('-', '_')
            mermaid += f"    participant {clean_actor}\n"
        
        mermaid += "\n"
        
        for interaction in interactions:
            from_actor = interaction.get('from', '').replace(' ', '_').replace('-', '_')
            to_actor = interaction.get('to', '').replace(' ', '_').replace('-', '_')
            message = interaction.get('message', 'interaction')
            arrow_type = interaction.get('type', '->')
            
            mermaid += f"    {from_actor}{arrow_type}{to_actor}: {message}\n"
        
        return mermaid
    
    @staticmethod
    def from_drawio_data(diagram_data: Dict) -> str:
        """Convert draw.io data to Mermaid sequence diagram"""
        actors = set()
        interactions = []
        
        shape_map = {shape['id']: shape['value'] for shape in diagram_data['shapes'] if shape['value']}
        
        for conn in diagram_data['connections']:
            source = shape_map.get(conn['source'], 'Unknown')
            target = shape_map.get(conn['target'], 'Unknown')
            message = conn['value'] or 'interaction'
            
            if source and target:
                actors.add(source)
                actors.add(target)
                
                interactions.append({
                    'from': source,
                    'to': target,
                    'message': message
                })
        
        if not actors:
            return "sequenceDiagram\n    participant A\n    participant B\n    A->>B: No connections found"
        
        return MermaidGenerator.generate_sequence_diagram(list(actors), interactions)


class JiraClient:
    """Jira API client for creating tickets"""
    
    def __init__(self, base_url: str, email: str, api_token: str):
        self.base_url = base_url.rstrip('/')
        self.auth = (email, api_token)
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def create_ticket(self, project_key: str, summary: str, description: str, 
                     issue_type: str = 'Task', **kwargs) -> Dict:
        """Create a Jira ticket"""
        url = f"{self.base_url}/rest/api/3/issue"
        
        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {"name": issue_type}
            }
        }
        
        if 'priority' in kwargs and kwargs['priority']:
            payload['fields']['priority'] = {'name': kwargs['priority']}
        if 'labels' in kwargs and kwargs['labels']:
            payload['fields']['labels'] = kwargs['labels']
        if 'assignee' in kwargs and kwargs['assignee']:
            payload['fields']['assignee'] = {'accountId': kwargs['assignee']}
        
        response = requests.post(url, json=payload, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        
        result = response.json()
        return {
            'key': result['key'],
            'id': result['id'],
            'url': f"{self.base_url}/browse/{result['key']}"
        }


class ConfluenceClient:
    """Confluence API client for creating pages"""
    
    def __init__(self, base_url: str, email: str, api_token: str):
        self.base_url = base_url.rstrip('/')
        self.auth = (email, api_token)
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def create_page(self, space_key: str, title: str, content: str, 
                   parent_id: Optional[str] = None) -> Dict:
        """Create a Confluence page"""
        url = f"{self.base_url}/rest/api/content"
        
        payload = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "body": {
                "storage": {
                    "value": content,
                    "representation": "storage"
                }
            }
        }
        
        if parent_id:
            payload['ancestors'] = [{"id": parent_id}]
        
        response = requests.post(url, json=payload, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        
        result = response.json()
        return {
            'id': result['id'],
            'url': f"{self.base_url}/pages/{result['id']}"
        }


class TemplateManager:
    """Manage Confluence page templates"""
    
    DEFAULT_TEMPLATES = {
        'technical': """
<h1>{title}</h1>
<h2>Overview</h2>
<p>{overview}</p>

<h2>Architecture Diagram</h2>
{diagram_description}

<h2>Sequence Flow</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">mermaid</ac:parameter>
  <ac:plain-text-body><![CDATA[{mermaid_diagram}]]></ac:plain-text-body>
</ac:structured-macro>

<h2>Components</h2>
<p>{components}</p>

<h2>Related Jira Ticket</h2>
<p>Implementation ticket: <ac:link>
  <ri:page ri:content-title="{jira_ticket}"/>
</ac:link></p>

<h2>Notes</h2>
<p>{notes}</p>
""",
        'simple': """
<h1>{title}</h1>
<p>{description}</p>

<h2>Diagram</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">mermaid</ac:parameter>
  <ac:plain-text-body><![CDATA[{mermaid_diagram}]]></ac:plain-text-body>
</ac:structured-macro>

<h2>Jira Ticket</h2>
<p><a href="{jira_url}">{jira_ticket}</a></p>
""",
        'detailed': """
<h1>{title}</h1>

<ac:structured-macro ac:name="info">
  <ac:rich-text-body>
    <p>This page was automatically generated from a diagram on {date}</p>
  </ac:rich-text-body>
</ac:structured-macro>

<h2>Executive Summary</h2>
<p>{summary}</p>

<h2>System Architecture</h2>
{diagram_description}

<h2>Sequence Diagram</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">mermaid</ac:parameter>
  <ac:plain-text-body><![CDATA[{mermaid_diagram}]]></ac:plain-text-body>
</ac:structured-macro>

<h2>Component Details</h2>
<table>
  <tr>
    <th>Component</th>
    <th>Description</th>
  </tr>
  {component_table}
</table>

<h2>Implementation</h2>
<p>Jira ticket: <a href="{jira_url}">{jira_ticket}</a></p>
<p>Status: {status}</p>

<h2>Additional Resources</h2>
<ul>
  {resources}
</ul>
"""
    }
    
    @classmethod
    def get_template(cls, template_name: str) -> str:
        """Get a template by name"""
        return cls.DEFAULT_TEMPLATES.get(template_name, cls.DEFAULT_TEMPLATES['simple'])
    
    @classmethod
    def apply_template(cls, template: str, variables: Dict) -> str:
        """Apply variables to a template"""
        result = template
        for key, value in variables.items():
            result = result.replace(f"{{{key}}}", str(value))
        return result
    
    @classmethod
    def list_templates(cls) -> List[str]:
        """List available templates"""
        return list(cls.DEFAULT_TEMPLATES.keys())


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '1.0.0'})


@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get available templates"""
    templates = TemplateManager.list_templates()
    return jsonify({
        'templates': templates,
        'default': 'simple'
    })


@app.route('/api/template/<template_name>', methods=['GET'])
def get_template(template_name):
    """Get a specific template"""
    template = TemplateManager.get_template(template_name)
    return jsonify({
        'name': template_name,
        'template': template
    })


@app.route('/api/process-drawio', methods=['POST'])
def process_drawio():
    """Process a single draw.io file"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Get configuration from form data
        config = json.loads(request.form.get('config', '{}'))
        project_key = request.form.get('projectKey')
        space_key = request.form.get('spaceKey')
        issue_type = request.form.get('issueType', 'Task')
        priority = request.form.get('priority', '')
        template_name = request.form.get('template', 'simple')
        parent_page_id = request.form.get('parentPageId', '')
        
        # Read file content
        file_content = file.read().decode('utf-8')
        
        # Parse draw.io file
        parser = DrawioParser(file_content)
        diagram_data = parser.parse()
        
        # Generate Mermaid diagram
        mermaid_diagram = MermaidGenerator.from_drawio_data(diagram_data)
        
        # Initialize clients
        jira_client = JiraClient(
            config.get('jiraUrl'),
            config.get('jiraEmail'),
            config.get('jiraToken')
        )
        
        confluence_client = ConfluenceClient(
            config.get('confluenceUrl'),
            config.get('jiraEmail'),
            config.get('jiraToken')
        )
        
        # Create Jira ticket
        ticket_summary = f"Implementation: {diagram_data['title']}"
        ticket_description = f"Diagram: {diagram_data['title']}\n\n"
        ticket_description += f"Components: {len(diagram_data['shapes'])}\n"
        ticket_description += f"Connections: {len(diagram_data['connections'])}\n\n"
        ticket_description += "See Confluence page for detailed sequence diagram."
        
        jira_ticket = jira_client.create_ticket(
            project_key=project_key,
            summary=ticket_summary,
            description=ticket_description,
            issue_type=issue_type,
            priority=priority if priority else None
        )
        
        # Create Confluence page
        template = TemplateManager.get_template(template_name)
        from datetime import datetime
        
        page_content = TemplateManager.apply_template(template, {
            'title': diagram_data['title'],
            'overview': f"This page documents the {diagram_data['title']} system architecture.",
            'description': f"System architecture with {len(diagram_data['shapes'])} components.",
            'diagram_description': f"<p>The diagram contains {len(diagram_data['shapes'])} components and {len(diagram_data['connections'])} connections.</p>",
            'mermaid_diagram': mermaid_diagram,
            'jira_ticket': jira_ticket['key'],
            'jira_url': jira_ticket['url'],
            'components': ', '.join([s['value'] for s in diagram_data['shapes'] if s['value']])[:200],
            'summary': f"Architecture overview for {diagram_data['title']}",
            'component_table': '<tr><td>Component</td><td>From diagram</td></tr>',
            'status': 'In Progress',
            'resources': '<li>Additional documentation pending</li>',
            'notes': 'Generated from draw.io diagram',
            'date': datetime.now().strftime('%Y-%m-%d')
        })
        
        confluence_page = confluence_client.create_page(
            space_key=space_key,
            title=diagram_data['title'],
            content=page_content,
            parent_id=parent_page_id if parent_page_id else None
        )
        
        return jsonify({
            'success': True,
            'jiraTicket': jira_ticket,
            'confluencePage': confluence_page,
            'mermaidDiagram': mermaid_diagram,
            'diagramData': diagram_data
        })
        
    except Exception as e:
        print(f"Error processing draw.io file: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/process-mermaid', methods=['POST'])
def process_mermaid():
    """Process a Mermaid diagram"""
    try:
        data = request.json
        
        mermaid_code = data.get('mermaidCode')
        config = data.get('config', {})
        project_key = data.get('projectKey')
        space_key = data.get('spaceKey')
        title = data.get('title', 'Sequence Diagram')
        issue_type = data.get('issueType', 'Task')
        priority = data.get('priority', '')
        template_name = data.get('template', 'simple')
        parent_page_id = data.get('parentPageId', '')
        
        if not mermaid_code:
            return jsonify({'error': 'No Mermaid code provided'}), 400
        
        # Initialize clients
        jira_client = JiraClient(
            config.get('jiraUrl'),
            config.get('jiraEmail'),
            config.get('jiraToken')
        )
        
        confluence_client = ConfluenceClient(
            config.get('confluenceUrl'),
            config.get('jiraEmail'),
            config.get('jiraToken')
        )
        
        # Create Jira ticket
        ticket_summary = f"Implementation: {title}"
        ticket_description = f"Sequence Diagram: {title}\n\nSee Confluence page for detailed diagram."
        
        jira_ticket = jira_client.create_ticket(
            project_key=project_key,
            summary=ticket_summary,
            description=ticket_description,
            issue_type=issue_type,
            priority=priority if priority else None
        )
        
        # Create Confluence page
        template = TemplateManager.get_template(template_name)
        from datetime import datetime
        
        page_content = TemplateManager.apply_template(template, {
            'title': title,
            'description': f"Sequence diagram for {title}",
            'overview': f"This page documents the {title} sequence flow.",
            'diagram_description': '<p>Sequence diagram showing system interactions.</p>',
            'mermaid_diagram': mermaid_code,
            'jira_ticket': jira_ticket['key'],
            'jira_url': jira_ticket['url'],
            'components': 'See diagram',
            'summary': f"Sequence flow for {title}",
            'component_table': '<tr><td>Component</td><td>From diagram</td></tr>',
            'status': 'In Progress',
            'resources': '<li>Additional documentation pending</li>',
            'notes': 'Generated from Mermaid diagram',
            'date': datetime.now().strftime('%Y-%m-%d')
        })
        
        confluence_page = confluence_client.create_page(
            space_key=space_key,
            title=title,
            content=page_content,
            parent_id=parent_page_id if parent_page_id else None
        )
        
        return jsonify({
            'success': True,
            'jiraTicket': jira_ticket,
            'confluencePage': confluence_page,
            'mermaidDiagram': mermaid_code
        })
        
    except Exception as e:
        print(f"Error processing Mermaid diagram: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/batch-process', methods=['POST'])
def batch_process():
    """Process multiple files at once"""
    try:
        if 'files[]' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files[]')
        config = json.loads(request.form.get('config', '{}'))
        project_key = request.form.get('projectKey')
        space_key = request.form.get('spaceKey')
        issue_type = request.form.get('issueType', 'Task')
        priority = request.form.get('priority', '')
        template_name = request.form.get('template', 'simple')
        parent_page_id = request.form.get('parentPageId', '')
        
        results = []
        errors = []
        
        jira_client = JiraClient(
            config.get('jiraUrl'),
            config.get('jiraEmail'),
            config.get('jiraToken')
        )
        
        confluence_client = ConfluenceClient(
            config.get('confluenceUrl'),
            config.get('jiraEmail'),
            config.get('jiraToken')
        )
        
        for file in files:
            try:
                if not allowed_file(file.filename):
                    errors.append({
                        'filename': file.filename,
                        'error': 'Invalid file type'
                    })
                    continue
                
                file_content = file.read().decode('utf-8')
                parser = DrawioParser(file_content)
                diagram_data = parser.parse()
                mermaid_diagram = MermaidGenerator.from_drawio_data(diagram_data)
                
                # Create Jira ticket
                ticket_summary = f"Implementation: {diagram_data['title']}"
                ticket_description = f"Diagram: {diagram_data['title']}\n\nComponents: {len(diagram_data['shapes'])}"
                
                jira_ticket = jira_client.create_ticket(
                    project_key=project_key,
                    summary=ticket_summary,
                    description=ticket_description,
                    issue_type=issue_type,
                    priority=priority if priority else None
                )
                
                # Create Confluence page
                template = TemplateManager.get_template(template_name)
                from datetime import datetime
                
                page_content = TemplateManager.apply_template(template, {
                    'title': diagram_data['title'],
                    'description': f"Architecture for {diagram_data['title']}",
                    'overview': f"System architecture documentation.",
                    'diagram_description': f"<p>{len(diagram_data['shapes'])} components, {len(diagram_data['connections'])} connections.</p>",
                    'mermaid_diagram': mermaid_diagram,
                    'jira_ticket': jira_ticket['key'],
                    'jira_url': jira_ticket['url'],
                    'components': ', '.join([s['value'] for s in diagram_data['shapes'] if s['value']])[:200],
                    'summary': f"Architecture overview",
                    'component_table': '',
                    'status': 'In Progress',
                    'resources': '',
                    'notes': 'Batch processed',
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
                
                confluence_page = confluence_client.create_page(
                    space_key=space_key,
                    title=diagram_data['title'],
                    content=page_content,
                    parent_id=parent_page_id if parent_page_id else None
                )
                
                results.append({
                    'filename': file.filename,
                    'jiraTicket': jira_ticket,
                    'confluencePage': confluence_page,
                    'success': True
                })
                
            except Exception as e:
                errors.append({
                    'filename': file.filename,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'processed': len(results),
            'failed': len(errors),
            'results': results,
            'errors': errors
        })
        
    except Exception as e:
        print(f"Error in batch processing: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/export-results', methods=['POST'])
def export_results():
    """Export batch processing results as CSV"""
    try:
        data = request.json
        results = data.get('results', [])
        
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Filename', 'Jira Ticket', 'Jira URL', 'Confluence Page ID', 'Confluence URL', 'Status'])
        
        # Write data
        for result in results:
            writer.writerow([
                result.get('filename', ''),
                result.get('jiraTicket', {}).get('key', ''),
                result.get('jiraTicket', {}).get('url', ''),
                result.get('confluencePage', {}).get('id', ''),
                result.get('confluencePage', {}).get('url', ''),
                'Success' if result.get('success') else 'Failed'
            ])
        
        output.seek(0)
        return output.getvalue(), 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=processing_results.csv'
        }
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Starting Flask server on http://localhost:5000")
    print("Available endpoints:")
    print("  GET  /api/health - Health check")
    print("  GET  /api/templates - List templates")
    print("  POST /api/process-drawio - Process draw.io file")
    print("  POST /api/process-mermaid - Process Mermaid diagram")
    print("  POST /api/batch-process - Batch process multiple files")
    print("  POST /api/export-results - Export results as CSV")
    
    app.run(debug=True, host='0.0.0.0', port=5000)