# Advanced Integration Examples

## 1. Email Notifications

Add email notifications when new applications are received:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_notification_email(tenant_data, screening_result):
    """Send email notification for new application"""
    
    sender_email = "your-email@gmail.com"
    sender_password = "your-app-password"
    recipient_email = "landlord@example.com"
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = f"New Rental Application: {tenant_data['full_name']}"
    
    body = f"""
    New rental application received!
    
    Applicant: {tenant_data['full_name']}
    Email: {tenant_data['email']}
    Phone: {tenant_data['phone']}
    Monthly Income: ${tenant_data['monthly_income']}
    Credit Score: {tenant_data['credit_score']}
    
    Screening Score: {screening_result['score']}/100
    Recommendation: {screening_result['recommendation'].upper()}
    
    View full application: http://localhost:5000/
    """
    
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# Add to app.py in the submit() function:
if agent.save_tenant_response(tenant_data):
    screening = agent.screen_tenant(tenant_data)
    send_notification_email(tenant_data, screening)  # Add this line
    return render_template('success.html', screening=screening)
```

## 2. SMS Notifications with Twilio

Get text messages for urgent applications:

```python
from twilio.rest import Client

def send_sms_notification(tenant_name, score):
    """Send SMS for high-priority applications"""
    
    # Your Twilio credentials
    account_sid = "your_account_sid"
    auth_token = "your_auth_token"
    twilio_number = "+1234567890"
    your_number = "+1987654321"
    
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        body=f"New rental application from {tenant_name}. Score: {score}/100. Check dashboard.",
        from_=twilio_number,
        to=your_number
    )
    
    return message.sid

# Add to submit() function for high-scoring applicants:
if screening['score'] >= 80:
    send_sms_notification(tenant_data['full_name'], screening['score'])
```

## 3. Google Sheets Integration

Automatically log applications to Google Sheets:

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def log_to_google_sheets(tenant_data, screening):
    """Log application to Google Sheets"""
    
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'credentials.json', scope)
    client = gspread.authorize(creds)
    
    sheet = client.open("Tenant Applications").sheet1
    
    row = [
        tenant_data['submitted_at'],
        tenant_data['full_name'],
        tenant_data['email'],
        tenant_data['phone'],
        tenant_data['monthly_income'],
        tenant_data['credit_score'],
        screening['score'],
        screening['recommendation']
    ]
    
    sheet.append_row(row)
```

## 4. Webhook Integration

Send data to other services via webhooks:

```python
import requests
import json

def send_webhook(tenant_data, screening):
    """Send application data to webhook URL"""
    
    webhook_url = "https://your-webhook-url.com/endpoint"
    
    payload = {
        "applicant": {
            "name": tenant_data['full_name'],
            "email": tenant_data['email'],
            "phone": tenant_data['phone']
        },
        "screening": {
            "score": screening['score'],
            "recommendation": screening['recommendation'],
            "flags": screening['flags']
        },
        "property": {
            "address": tenant_data['property_address']
        }
    }
    
    try:
        response = requests.post(
            webhook_url,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Webhook failed: {e}")
        return False
```

## 5. Slack Notifications

Get notifications in your Slack workspace:

```python
import requests
import json

def send_slack_notification(tenant_data, screening):
    """Send notification to Slack channel"""
    
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    
    color = "#36a64f" if screening['score'] >= 70 else "#ff9800"
    
    message = {
        "text": "New Rental Application Received! 🏠",
        "attachments": [
            {
                "color": color,
                "fields": [
                    {
                        "title": "Applicant",
                        "value": tenant_data['full_name'],
                        "short": True
                    },
                    {
                        "title": "Score",
                        "value": f"{screening['score']}/100",
                        "short": True
                    },
                    {
                        "title": "Email",
                        "value": tenant_data['email'],
                        "short": True
                    },
                    {
                        "title": "Income",
                        "value": f"${tenant_data['monthly_income']}",
                        "short": True
                    },
                    {
                        "title": "Recommendation",
                        "value": screening['recommendation'].upper(),
                        "short": True
                    }
                ],
                "footer": "Tenant Monitoring Agent"
            }
        ]
    }
    
    response = requests.post(webhook_url, data=json.dumps(message))
    return response.status_code == 200
```

## 6. Calendar Integration

Schedule property viewings automatically:

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

def schedule_viewing(tenant_data):
    """Create Google Calendar event for property viewing"""
    
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    
    # Schedule viewing for 2 days from now
    start_time = datetime.now() + timedelta(days=2)
    end_time = start_time + timedelta(hours=1)
    
    event = {
        'summary': f'Property Viewing - {tenant_data["full_name"]}',
        'description': f'Viewing for {tenant_data["property_address"]}',
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/New_York',
        },
        'attendees': [
            {'email': tenant_data['email']},
        ],
    }
    
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')
```

## 7. Database Storage (SQLite)

Store applications in a database instead of JSON:

```python
import sqlite3
from datetime import datetime

def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect('tenants.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            monthly_income REAL,
            credit_score INTEGER,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            screening_score INTEGER,
            recommendation TEXT,
            property_address TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_to_database(tenant_data, screening):
    """Save application to database"""
    conn = sqlite3.connect('tenants.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO applications 
        (full_name, email, phone, monthly_income, credit_score, 
         screening_score, recommendation, property_address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        tenant_data['full_name'],
        tenant_data['email'],
        tenant_data['phone'],
        tenant_data['monthly_income'],
        tenant_data['credit_score'],
        screening['score'],
        screening['recommendation'],
        tenant_data['property_address']
    ))
    
    conn.commit()
    conn.close()

def get_all_from_database():
    """Retrieve all applications from database"""
    conn = sqlite3.connect('tenants.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM applications ORDER BY submitted_at DESC')
    rows = cursor.fetchall()
    
    applications = [dict(row) for row in rows]
    conn.close()
    
    return applications
```

## 8. Document Upload with AWS S3

Allow tenants to upload documents:

```python
import boto3
from werkzeug.utils import secure_filename

s3_client = boto3.client(
    's3',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY'
)

@app.route('/upload-document', methods=['POST'])
def upload_document():
    """Handle document uploads"""
    
    if 'document' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['document']
    applicant_id = request.form.get('applicant_id')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    filename = secure_filename(file.filename)
    s3_key = f"applications/{applicant_id}/{filename}"
    
    try:
        s3_client.upload_fileobj(
            file,
            'your-bucket-name',
            s3_key
        )
        return jsonify({
            'success': True,
            'url': f"https://your-bucket-name.s3.amazonaws.com/{s3_key}"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

## 9. Automated Background Check API

Integrate with TransUnion or Checkr:

```python
import requests

def run_background_check(tenant_data):
    """Run automated background check via API"""
    
    api_key = "YOUR_API_KEY"
    api_url = "https://api.backgroundcheck.com/v1/checks"
    
    payload = {
        "first_name": tenant_data['full_name'].split()[0],
        "last_name": tenant_data['full_name'].split()[-1],
        "email": tenant_data['email'],
        "phone": tenant_data['phone'],
        "package": "basic_criminal_check"
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(api_url, json=payload, headers=headers)
    
    if response.status_code == 201:
        return response.json()
    else:
        return {"error": "Background check failed"}
```

## 10. Multi-language Support

Support applications in multiple languages:

```python
from flask_babel import Babel, gettext

babel = Babel(app)

LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'zh': 'Chinese'
}

@babel.localeselector
def get_locale():
    return request.args.get('lang') or request.accept_languages.best_match(LANGUAGES.keys())

# In templates, use:
# {{ gettext('Full Name') }}
# {{ gettext('Email Address') }}
```

## Installation for Advanced Features

```bash
# Email
pip install secure-smtplib --break-system-packages

# SMS (Twilio)
pip install twilio --break-system-packages

# Google Sheets
pip install gspread oauth2client --break-system-packages

# Database
pip install sqlalchemy --break-system-packages

# AWS S3
pip install boto3 --break-system-packages

# Multi-language
pip install Flask-Babel --break-system-packages
```

## Complete Integration Example

Here's how to integrate multiple services into your submit() function:

```python
@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission with all integrations"""
    try:
        tenant_data = {
            # ... collect form data ...
        }
        
        # Save to database
        if agent.save_tenant_response(tenant_data):
            
            # Screen the tenant
            screening = agent.screen_tenant(tenant_data)
            
            # Send notifications
            send_notification_email(tenant_data, screening)
            
            # High-priority applications get SMS
            if screening['score'] >= 80:
                send_sms_notification(tenant_data['full_name'], screening['score'])
            
            # Log to Google Sheets
            log_to_google_sheets(tenant_data, screening)
            
            # Notify Slack channel
            send_slack_notification(tenant_data, screening)
            
            # Send to webhook
            send_webhook(tenant_data, screening)
            
            # Schedule viewing for qualified applicants
            if screening['recommendation'] == 'approve':
                viewing_link = schedule_viewing(tenant_data)
            
            return render_template('success.html', screening=screening)
        else:
            return "Error submitting form", 500
            
    except Exception as e:
        print(f"Error processing form: {e}")
        return f"Error processing form: {str(e)}", 500
```

Remember to handle errors gracefully and store API credentials securely using environment variables!
