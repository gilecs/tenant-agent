"""
Facebook Marketplace Property Listing Monitor & Tenant Form Agent

This agent monitors Facebook Marketplace messages for your property listing
and automatically responds to potential tenants with a form to collect initial information.

Requirements:
- Facebook account with Marketplace listing
- Flask for web interface
- Storage for tenant responses

Note: Direct Facebook API access for Marketplace is limited. This provides a framework
that can be integrated with Facebook's official tools or manual monitoring.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
import os

class TenantFormAgent:
    """Agent to manage tenant inquiries and form collection"""
    
    def __init__(self, property_details: Dict[str, str]):
        self.property_details = property_details
        self.responses_file = "tenant_responses.json"
        self.auto_response_template = self._create_response_template()
        
    def _create_response_template(self) -> str:
        """Create the automated response message with form link"""
        return f"""
Hi! Thank you for your interest in our property at {self.property_details.get('address', 'this location')}.

To help us process your inquiry quickly, please fill out this brief form with your information:

📋 Tenant Application Form:
{self.property_details.get('form_url', '[FORM_URL_HERE]')}

The form takes just 2-3 minutes and asks for:
✓ Contact information
✓ Move-in date
✓ Income verification
✓ Rental history
✓ Number of occupants

Once submitted, I'll review your application and get back to you within 24 hours.

Looking forward to hearing from you!

Property Details:
• Address: {self.property_details.get('address', 'N/A')}
• Rent: ${self.property_details.get('rent', 'N/A')}/month
• Bedrooms: {self.property_details.get('bedrooms', 'N/A')}
• Bathrooms: {self.property_details.get('bathrooms', 'N/A')}
• Available: {self.property_details.get('available_date', 'N/A')}
"""
    
    def get_auto_response(self, inquiry_message: str = None) -> str:
        """
        Generate automated response based on inquiry
        
        Args:
            inquiry_message: Optional message from potential tenant
            
        Returns:
            Automated response text
        """
        return self.auto_response_template
    
    def save_tenant_response(self, tenant_data: Dict) -> bool:
        """
        Save tenant form response to storage
        
        Args:
            tenant_data: Dictionary containing tenant information
            
        Returns:
            Success status
        """
        try:
            # Load existing responses
            if os.path.exists(self.responses_file):
                with open(self.responses_file, 'r') as f:
                    responses = json.load(f)
            else:
                responses = []
            
            # Add timestamp
            tenant_data['submitted_at'] = datetime.now().isoformat()
            tenant_data['property_address'] = self.property_details.get('address')
            
            # Append new response
            responses.append(tenant_data)
            
            # Save back to file
            with open(self.responses_file, 'w') as f:
                json.dump(responses, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving tenant response: {e}")
            return False
    
    def get_all_responses(self) -> List[Dict]:
        """Retrieve all tenant responses"""
        try:
            if os.path.exists(self.responses_file):
                with open(self.responses_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading responses: {e}")
            return []
    
    def screen_tenant(self, tenant_data: Dict) -> Dict[str, any]:
        """
        Basic tenant screening based on form data
        
        Returns:
            Dictionary with screening results and flags
        """
        flags = []
        score = 100
        
        # Income check (should be 3x rent)
        monthly_income = tenant_data.get('monthly_income', 0)
        required_income = float(self.property_details.get('rent', 0)) * 3
        
        if monthly_income < required_income:
            flags.append(f"Income below 3x rent requirement (${monthly_income} < ${required_income})")
            score -= 30
        
        # Move-in date compatibility
        desired_date = tenant_data.get('desired_move_in_date', '')
        available_date = self.property_details.get('available_date', '')
        
        # Credit score check
        credit_score = tenant_data.get('credit_score', 0)
        if credit_score < 650:
            flags.append(f"Credit score below preferred threshold ({credit_score})")
            score -= 20
        
        # Rental history
        if not tenant_data.get('has_rental_history', False):
            flags.append("No rental history provided")
            score -= 10
        
        # Eviction history
        if tenant_data.get('has_evictions', False):
            flags.append("Previous evictions reported")
            score -= 40
        
        return {
            'score': max(score, 0),
            'flags': flags,
            'recommendation': 'approve' if score >= 70 else 'review' if score >= 50 else 'deny',
            'tenant_data': tenant_data
        }


# Flask web application for the form
FLASK_APP_CODE = '''
from flask import Flask, render_template, request, jsonify, redirect, url_for
from facebook_marketplace_agent import TenantFormAgent

app = Flask(__name__)

# Initialize agent with your property details
property_details = {
    'address': '123 Main Street, Apt 2B, City, State 12345',
    'rent': '1500',
    'bedrooms': '2',
    'bathrooms': '1',
    'available_date': 'March 1, 2026',
    'form_url': 'http://localhost:5000/form'
}

agent = TenantFormAgent(property_details)

@app.route('/')
def index():
    """Dashboard showing all tenant applications"""
    responses = agent.get_all_responses()
    return render_template('dashboard.html', responses=responses)

@app.route('/form')
def form():
    """Tenant application form"""
    return render_template('tenant_form.html', property=property_details)

@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission"""
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

@app.route('/api/auto-response')
def auto_response():
    """API endpoint to get auto-response text"""
    return jsonify({'response': agent.get_auto_response()})

@app.route('/api/screening/<int:response_id>')
def get_screening(response_id):
    """Get screening results for a specific application"""
    responses = agent.get_all_responses()
    if response_id < len(responses):
        screening = agent.screen_tenant(responses[response_id])
        return jsonify(screening)
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''

def main():
    """Example usage"""
    
    # Initialize agent with your property details
    property_details = {
        'address': '123 Main Street, Apt 2B',
        'rent': '1500',
        'bedrooms': '2',
        'bathrooms': '1',
        'available_date': 'March 1, 2026',
        'form_url': 'http://localhost:5000/form'
    }
    
    agent = TenantFormAgent(property_details)
    
    # Get the auto-response message
    print("=" * 60)
    print("AUTO-RESPONSE MESSAGE FOR FACEBOOK MARKETPLACE")
    print("=" * 60)
    print(agent.get_auto_response())
    print("=" * 60)
    
    # Example: Save a tenant response
    example_tenant = {
        'full_name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': '555-0123',
        'monthly_income': 5000,
        'credit_score': 720,
        'has_rental_history': True,
        'has_evictions': False,
        'num_occupants': 2
    }
    
    agent.save_tenant_response(example_tenant)
    
    # Screen the tenant
    screening = agent.screen_tenant(example_tenant)
    print("\nTENANT SCREENING RESULT:")
    print(f"Score: {screening['score']}/100")
    print(f"Recommendation: {screening['recommendation'].upper()}")
    if screening['flags']:
        print(f"Flags: {', '.join(screening['flags'])}")
    else:
        print("No flags raised")

if __name__ == '__main__':
    main()
