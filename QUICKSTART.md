# 🚀 QUICK START GUIDE

## What This Does

This agent automates your Facebook Marketplace property listing tenant management:
1. Provides a professional auto-response message for FB Marketplace inquiries
2. Directs potential tenants to fill out a comprehensive online form
3. Automatically screens applicants based on income, credit, and history
4. Organizes all applications in an easy-to-use dashboard

## Getting Started in 5 Minutes

### Step 1: Install (30 seconds)
```bash
cd tenant-agent
pip install flask --break-system-packages
```

Or run the setup script:
```bash
bash setup.sh
```

### Step 2: Configure Your Property (2 minutes)

Open `app.py` and update lines 11-17 with YOUR property details:

```python
property_details = {
    'address': '123 Main Street, Apt 2B, City, State 12345',  # ← Your address
    'rent': '1500',                                            # ← Your rent
    'bedrooms': '2',                                           # ← Bedrooms
    'bathrooms': '1',                                          # ← Bathrooms
    'available_date': 'March 1, 2026',                        # ← Available date
    'form_url': 'http://localhost:5000/form'                  # ← Keep this for now
}
```

### Step 3: Run the Application (10 seconds)
```bash
python3 app.py
```

You should see:
```
============================================================
Facebook Marketplace Tenant Monitoring Agent
============================================================
🌐 Server starting...
📊 Dashboard: http://localhost:5000/
```

### Step 4: Test It (1 minute)

Open your browser and visit:
- http://localhost:5000/test ← Start here to verify setup
- http://localhost:5000/form ← This is what tenants will see
- http://localhost:5000/ ← Your application dashboard

### Step 5: Use with Facebook Marketplace (1 minute)

1. Visit http://localhost:5000/api/auto-response
2. Copy the message shown
3. When someone messages you on Facebook Marketplace, paste this response
4. They click the link and fill out the form
5. Check your dashboard at http://localhost:5000/ to see their application!

## What Each File Does

- **facebook_marketplace_agent.py** - Core logic for screening and managing applications
- **app.py** - Web server that runs everything
- **templates/tenant_form.html** - The form tenants fill out
- **templates/dashboard.html** - Where you view applications
- **templates/success.html** - Confirmation page after form submission
- **README.md** - Comprehensive documentation
- **INTEGRATIONS.md** - Advanced features (email, SMS, etc.)

## Common Questions

**Q: Can tenants see other applications?**
A: No, tenants only see the form. Only you can see the dashboard.

**Q: Do I need to keep my computer on?**
A: For testing, yes. For production, deploy to a cloud service (see README.md deployment section).

**Q: How do I make the form accessible from anywhere?**
A: Either:
- Use ngrok (easiest for testing): `ngrok http 5000`
- Deploy to cloud (best for production - see README.md)

**Q: Where is the data stored?**
A: In a file called `tenant_responses.json` in the same folder.

**Q: Can I customize the form fields?**
A: Yes! Edit `templates/tenant_form.html` and update the screening logic in `facebook_marketplace_agent.py`.

**Q: Is this secure for collecting personal information?**
A: For local testing only. For real use, deploy with HTTPS (see README.md security section).

## Need Help?

- Full documentation: See README.md
- Advanced features: See INTEGRATIONS.md
- Issues: Check that Flask is installed and all files are present

## Next Steps

1. ✅ Test the setup with a fake application
2. 📱 Try ngrok to make it accessible from your phone
3. ☁️ Deploy to a cloud service for real use
4. 🔔 Add email notifications (see INTEGRATIONS.md)
5. 🎨 Customize the form and screening criteria

---

**Remember:** This is a tool to help manage applications. Always review applications carefully and comply with fair housing laws. Don't discriminate based on protected classes.
