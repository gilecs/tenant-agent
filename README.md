# Facebook Marketplace Property Listing Monitor & Tenant Form Agent

## 🎯 Overview

This automated agent helps property owners manage tenant inquiries from Facebook Marketplace by:
- Providing automated responses to potential tenants
- Collecting tenant information through a professional online form
- Screening applicants based on customizable criteria
- Organizing all applications in an easy-to-use dashboard

## 📋 Features

### ✅ Automated Response System
- Pre-written professional response message
- Includes property details and form link
- Consistent communication with all inquiries

### 📝 Tenant Application Form
- Mobile-friendly design
- Collects essential information:
  - Personal details (name, email, phone)
  - Employment and income verification
  - Credit score range
  - Rental history
  - Background information
  - Pet information
  - Move-in preferences

### 🔍 Automated Screening
- Income-to-rent ratio check (3x rule)
- Credit score evaluation
- Rental history verification
- Eviction history check
- Automatic scoring (0-100)
- Recommendation system (approve/review/deny)

### 📊 Dashboard
- View all applications in one place
- Filter and sort applicants
- See screening scores at a glance
- Quick access to contact information

## 🚀 Quick Start Guide

### 1. Installation

```bash
# Install required packages
pip install flask --break-system-packages

# Create project directory
mkdir tenant-agent
cd tenant-agent

# Copy all provided files into this directory
# - facebook_marketplace_agent.py
# - app.py
# - templates/tenant_form.html
# - templates/success.html
# - templates/dashboard.html
```

### 2. Configure Your Property Details

Edit `app.py` and update the `property_details` dictionary:

```python
property_details = {
    'address': 'YOUR PROPERTY ADDRESS',
    'rent': 'MONTHLY RENT AMOUNT (numbers only)',
    'bedrooms': 'NUMBER OF BEDROOMS',
    'bathrooms': 'NUMBER OF BATHROOMS',
    'available_date': 'AVAILABLE DATE',
    'form_url': 'http://localhost:5000/form'  # Update when deployed
}
```

Example:
```python
property_details = {
    'address': '456 Oak Street, Apt 3A, Boston, MA 02101',
    'rent': '2200',
    'bedrooms': '3',
    'bathrooms': '2',
    'available_date': 'April 1, 2026',
    'form_url': 'http://localhost:5000/form'
}
```

### 3. Run the Application

```bash
python app.py
```

You should see:
```
============================================================
Facebook Marketplace Tenant Monitoring Agent
============================================================

🏠 Property: [Your Property Address]
💰 Rent: $[Amount]/month

🌐 Server starting...
📊 Dashboard: http://localhost:5000/
📋 Form: http://localhost:5000/form
🧪 Test: http://localhost:5000/test
🤖 Auto-response: http://localhost:5000/api/auto-response

============================================================
```

### 4. Test the Setup

Open your browser and visit:
- `http://localhost:5000/test` - Verify everything is working
- `http://localhost:5000/form` - See the tenant form
- `http://localhost:5000/` - View the dashboard

## 📱 How to Use with Facebook Marketplace

### Method 1: Manual Response (Recommended)

1. When you receive a message on Facebook Marketplace about your listing
2. Visit `http://localhost:5000/api/auto-response` to get your response message
3. Copy the message
4. Paste it as a reply to the Facebook Marketplace inquiry
5. The potential tenant clicks the form link and fills it out
6. View their application in your dashboard at `http://localhost:5000/`

### Method 2: Automated Setup (Advanced)

**Note:** Facebook doesn't provide direct API access to Marketplace messages for this use case. However, you can use:

1. **Facebook Messenger API** (requires business verification)
   - Set up a Facebook Business account
   - Get API access
   - Integrate with the agent using webhooks

2. **Browser automation tools** (use carefully)
   - Tools like Selenium can automate browser actions
   - Must comply with Facebook's Terms of Service
   - Not recommended for production use

3. **Third-party tools**
   - ManyChat, Chatfuel, or similar platforms
   - Can integrate with this system via webhooks

## 🎨 Customization Options

### Modify Screening Criteria

Edit the `screen_tenant()` method in `facebook_marketplace_agent.py`:

```python
def screen_tenant(self, tenant_data: Dict) -> Dict[str, any]:
    flags = []
    score = 100
    
    # Customize income requirement (default: 3x rent)
    required_income = float(self.property_details.get('rent', 0)) * 3
    
    # Customize credit score threshold (default: 650)
    if credit_score < 650:
        flags.append(f"Credit score below preferred threshold")
        score -= 20
    
    # Add your own criteria here
    # ...
```

### Customize Form Fields

Edit `templates/tenant_form.html` to add or remove fields. Don't forget to update the form submission handler in `app.py`.

### Change Auto-Response Message

Edit the `_create_response_template()` method in `facebook_marketplace_agent.py`:

```python
def _create_response_template(self) -> str:
    return f"""
    Your custom message here...
    """
```

## 🌐 Deployment Options

### Option 1: Deploy to Cloud (Recommended)

**Heroku:**
```bash
# Install Heroku CLI
# Login: heroku login
heroku create your-app-name
git push heroku main
```

**DigitalOcean App Platform:**
1. Connect your GitHub repository
2. Select Python as runtime
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `python app.py`

**Railway:**
1. Connect GitHub repository
2. Automatic deployment
3. Get your public URL

**Update form_url** in `property_details` to your deployed URL!

### Option 2: Use ngrok (For Testing)

```bash
# Install ngrok: https://ngrok.com/
ngrok http 5000

# Use the provided URL (e.g., https://abc123.ngrok.io)
# Update form_url in app.py with this URL
```

### Option 3: Keep Local

Only accessible from your computer. Good for testing but not for real tenant applications.

## 📊 Data Storage

Applications are stored in `tenant_responses.json` in the same directory as the app.

**Format:**
```json
[
  {
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "555-0123",
    "submitted_at": "2026-02-06T10:30:00",
    "property_address": "123 Main St",
    "monthly_income": 5000,
    "credit_score": 720,
    ...
  }
]
```

### Backup Your Data

```bash
# Make regular backups
cp tenant_responses.json tenant_responses_backup_$(date +%Y%m%d).json
```

## 🔒 Security Considerations

1. **HTTPS Required for Production**
   - Never collect sensitive information over HTTP
   - Use SSL certificates (Let's Encrypt is free)

2. **Data Privacy**
   - This collects personal information
   - Comply with privacy laws (GDPR, CCPA, etc.)
   - Have a privacy policy
   - Securely delete data when no longer needed

3. **Access Control**
   - Add authentication to the dashboard
   - Don't expose the dashboard publicly without login

4. **Rate Limiting**
   - Implement rate limiting to prevent spam
   - Use CAPTCHA on the form

Example: Add basic authentication to dashboard:
```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

users = {
    "admin": "your-secure-password"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
@auth.login_required
def index():
    # Dashboard code...
```

## 🛠️ Troubleshooting

### "Module not found" Error
```bash
pip install flask --break-system-packages
```

### Form not submitting
- Check browser console for errors (F12)
- Verify all required fields are filled
- Check terminal for Python errors

### Can't access from other devices
- Use `0.0.0.0` instead of `127.0.0.1`
- Check firewall settings
- Use ngrok or deploy to cloud

### Data not saving
- Check file permissions
- Verify `tenant_responses.json` can be created
- Check disk space

## 📧 Support & Next Steps

### Enhancements You Could Add

1. **Email Notifications**
   - Get notified when new applications arrive
   - Send automated responses to applicants

2. **SMS Integration**
   - Text message notifications
   - Two-way communication with Twilio

3. **Document Upload**
   - Allow tenants to upload ID, pay stubs
   - Integrate with cloud storage

4. **Calendar Integration**
   - Schedule property viewings
   - Sync with Google Calendar

5. **Payment Processing**
   - Collect application fees
   - Security deposit handling

6. **Background Check APIs**
   - Integrate with TransUnion, Experian
   - Automated verification

7. **Multi-property Support**
   - Manage multiple listings
   - Property-specific forms

## 📝 Example Auto-Response

Here's what gets sent to potential tenants:

```
Hi! Thank you for your interest in our property at 123 Main Street, Apt 2B, City, State 12345.

To help us process your inquiry quickly, please fill out this brief form with your information:

📋 Tenant Application Form:
http://localhost:5000/form

The form takes just 2-3 minutes and asks for:
✓ Contact information
✓ Move-in date
✓ Income verification
✓ Rental history
✓ Number of occupants

Once submitted, I'll review your application and get back to you within 24 hours.

Looking forward to hearing from you!

Property Details:
• Address: 123 Main Street, Apt 2B, City, State 12345
• Rent: $1500/month
• Bedrooms: 2
• Bathrooms: 1
• Available: March 1, 2026
```

## 🎓 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Facebook Messenger API](https://developers.facebook.com/docs/messenger-platform)
- [Fair Housing Laws](https://www.hud.gov/program_offices/fair_housing_equal_opp)
- [Landlord-Tenant Law Guide](https://www.nolo.com/legal-encyclopedia/landlords-tenants)

## ⚖️ Legal Disclaimer

This tool is for informational purposes only. As a landlord:
- Comply with all fair housing laws
- Don't discriminate based on protected classes
- Follow your local tenant screening laws
- Consult with an attorney for legal advice
- Review your local and state regulations

Automated screening is a tool to assist decision-making, not replace it. Always review applications carefully and fairly.

---

**Questions?** Open an issue or refer to the Flask documentation for technical questions.
