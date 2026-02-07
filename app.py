from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from facebook_marketplace_agent import TenantFormAgent

app = Flask(__name__)

# Initialize agent with your property details
# UPDATE THESE WITH YOUR ACTUAL PROPERTY INFORMATION
property_details = {
    'address': 'Quincy, MA, 02169',
    'rent': '3200',
    'bedrooms': '1',
    'bathrooms': '2',
    'available_date': 'February 1, 2026',
    'form_url': 'https://tenant-agent.onrender.com/form'  # Update with your actual URL when deployed
}

agent = TenantFormAgent(property_details)

@app.route('/')
def index():
    """Dashboard showing all tenant applications"""
    responses = agent.get_all_responses()
    return render_template('dashboard.html', responses=responses, property=property_details)

@app.route('/form')
def form():
    """Tenant application form"""
    return render_template('tenant_form.html', property=property_details)

@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission"""
    try:
        tenant_data = {
            'full_name': request.form.get('full_name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'current_address': request.form.get('current_address'),
            'desired_move_in_date': request.form.get('move_in_date'),
            'monthly_income': float(request.form.get('monthly_income', 0)),
            'employer': request.form.get('employer'),
            'credit_score': int(request.form.get('credit_score', 0)),
            'num_occupants': int(request.form.get('num_occupants', 1)),
            'has_pets': request.form.get('has_pets') == 'yes',
            'pet_details': request.form.get('pet_details', ''),
            'has_rental_history': request.form.get('has_rental_history') == 'yes',
            'previous_landlord': request.form.get('previous_landlord', ''),
            'previous_landlord_phone': request.form.get('previous_landlord_phone', ''),
            'has_evictions': request.form.get('has_evictions') == 'yes',
            'additional_info': request.form.get('additional_info', '')
        }
        
        if agent.save_tenant_response(tenant_data):
            # Screen the tenant
            screening = agent.screen_tenant(tenant_data)
            return render_template('success.html', screening=screening)
        else:
            return "Error submitting form", 500
    except Exception as e:
        print(f"Error processing form: {e}")
        return f"Error processing form: {str(e)}", 500

@app.route('/api/auto-response')
def auto_response():
    """API endpoint to get auto-response text for Facebook Marketplace"""
    return jsonify({
        'response': agent.get_auto_response(),
        'success': True
    })

@app.route('/api/responses')
def get_responses():
    """API endpoint to get all tenant responses"""
    responses = agent.get_all_responses()
    return jsonify({
        'responses': responses,
        'count': len(responses)
    })

@app.route('/api/screening/<int:response_id>')
def get_screening(response_id):
    """Get screening results for a specific application"""
    responses = agent.get_all_responses()
    if response_id < len(responses):
        screening = agent.screen_tenant(responses[response_id])
        return jsonify(screening)
    return jsonify({'error': 'Application not found'}), 404

@app.route('/test')
def test():
    """Test page to verify setup"""
    return f"""
    <html>
    <head>
        <title>Test Page</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
            h1 {{ color: #667eea; }}
            .success {{ background: #e8f5e9; padding: 15px; border-radius: 5px; margin: 10px 0; }}
            .info {{ background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 10px 0; }}
            a {{ color: #667eea; text-decoration: none; font-weight: bold; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1>✅ Facebook Marketplace Tenant Agent - Setup Test</h1>
        <div class="success">
            <strong>Success!</strong> Your application is running correctly.
        </div>
        <div class="info">
            <h3>Available Pages:</h3>
            <ul>
                <li><a href="/">Dashboard</a> - View all tenant applications</li>
                <li><a href="/form">Application Form</a> - The form tenants will fill out</li>
                <li><a href="/api/auto-response">Auto-Response API</a> - Get the message to post on Facebook</li>
            </ul>
        </div>
        <div class="info">
            <h3>Property Details:</h3>
            <p><strong>Address:</strong> {property_details['address']}</p>
            <p><strong>Rent:</strong> ${property_details['rent']}/month</p>
            <p><strong>Bedrooms:</strong> {property_details['bedrooms']}</p>
            <p><strong>Bathrooms:</strong> {property_details['bathrooms']}</p>
            <p><strong>Available:</strong> {property_details['available_date']}</p>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    # This runs for local development only
    # In production (Render), gunicorn is used instead
    print("=" * 60)
    print("Facebook Marketplace Tenant Monitoring Agent")
    print("=" * 60)
    print(f"\n🏠 Property: {property_details['address']}")
    print(f"💰 Rent: ${property_details['rent']}/month")
    print(f"\n🌐 Server starting...")
    print(f"📊 Dashboard: http://localhost:5000/")
    print(f"📋 Form: http://localhost:5000/form")
    print(f"🧪 Test: http://localhost:5000/test")
    print(f"🤖 Auto-response: http://localhost:5000/api/auto-response")
    print("\n" + "=" * 60)
    print("\nPress Ctrl+C to stop the server\n")
    
    # Get port from environment variable (for cloud deployment) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
