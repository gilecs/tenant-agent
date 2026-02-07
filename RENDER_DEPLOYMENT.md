# 🚀 Complete Render.com Deployment Guide (100% Free)

## ⏱️ Total Time: 10 minutes

This guide will walk you through deploying your Facebook Marketplace Tenant Agent to Render.com for **completely free**. No credit card required.

---

## 📋 Prerequisites Checklist

Before starting, make sure you have:
- [ ] All the agent files downloaded
- [ ] A GitHub account (free - we'll create one if you don't have it)
- [ ] 10 minutes of time

---

## Part 1: Prepare Your Files (3 minutes)

### Step 1: Create Required Files

First, we need to add a few files that Render needs. Create these in your `tenant-agent` folder:

#### File 1: `render.yaml`
Create a new file called `render.yaml` with this content:

```yaml
services:
  - type: web
    name: tenant-agent
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

#### File 2: Update `requirements.txt`
Replace your `requirements.txt` content with this:

```txt
Flask==3.0.0
Werkzeug==3.0.1
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
gunicorn==21.2.0
```

#### File 3: Create `.gitignore`
Create a file called `.gitignore`:

```txt
*.pyc
__pycache__/
tenant_responses.json
.env
.DS_Store
*.db
```

#### File 4: Update `app.py` 
Change the last line of `app.py` from:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

To:
```python
if __name__ == '__main__':
    # For local development
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**Important:** Also update the `form_url` in `app.py`:
```python
property_details = {
    'address': 'YOUR ADDRESS HERE',
    'rent': 'YOUR RENT',
    'bedrooms': 'X',
    'bathrooms': 'X',
    'available_date': 'DATE',
    'form_url': 'https://YOUR-APP-NAME.onrender.com/form'  # ← We'll update this
}
```

---

## Part 2: Upload to GitHub (4 minutes)

### Option A: Using GitHub Website (Easier)

1. **Go to GitHub**
   - Visit https://github.com
   - Sign up for free if you don't have an account
   - Click "Sign in" if you already have an account

2. **Create a New Repository**
   - Click the "+" icon in top right
   - Select "New repository"
   - Name it: `tenant-agent`
   - Description: "Facebook Marketplace tenant application system"
   - Keep it **Public** (required for free deployment)
   - ✅ Check "Add a README file"
   - Click "Create repository"

3. **Upload Your Files**
   - Click "Add file" → "Upload files"
   - Drag and drop ALL your files:
     * facebook_marketplace_agent.py
     * app.py
     * requirements.txt
     * render.yaml
     * .gitignore
     * setup.sh
     * README.md
     * QUICKSTART.md
     * INTEGRATIONS.md
     * The entire `templates` folder
   - Scroll down, write commit message: "Initial commit"
   - Click "Commit changes"

4. **Verify Upload**
   - You should see all your files listed
   - Make sure the `templates` folder is there with all 3 HTML files inside

### Option B: Using Git Command Line (For Advanced Users)

```bash
# Navigate to your project folder
cd tenant-agent

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Create repo on GitHub first (via website), then:
git remote add origin https://github.com/YOUR-USERNAME/tenant-agent.git
git branch -M main
git push -u origin main
```

---

## Part 3: Deploy to Render (3 minutes)

### Step 1: Create Render Account

1. **Go to Render**
   - Visit https://render.com
   - Click "Get Started" or "Sign Up"

2. **Sign Up Options**
   - Click "Sign up with GitHub" (easiest option)
   - Or use email if you prefer
   - Complete the verification

3. **Authorize GitHub**
   - Render will ask to access your GitHub
   - Click "Authorize Render"
   - This lets Render see your repositories

### Step 2: Create Web Service

1. **From Dashboard**
   - You'll see the Render dashboard
   - Click "New +" button (top right)
   - Select "Web Service"

2. **Connect Repository**
   - You'll see a list of your GitHub repos
   - Find "tenant-agent"
   - Click "Connect"
   
   **Don't see your repo?**
   - Click "Configure account" link
   - Grant Render access to your repositories
   - Go back and refresh

3. **Configure Your Service**

   Fill in these fields:

   **Name:** `tenant-agent` (or anything you like)
   - This becomes your URL: `https://tenant-agent.onrender.com`
   - Must be unique across all Render apps
   - If taken, try: `tenant-agent-yourname` or `property-manager-2024`

   **Region:** Choose closest to you
   - US (Oregon, Ohio, Virginia)
   - Europe (Frankfurt)
   - Singapore

   **Branch:** `main`

   **Root Directory:** Leave blank

   **Runtime:** Auto-detected (should show Python)

   **Build Command:** 
   ```
   pip install -r requirements.txt
   ```

   **Start Command:**
   ```
   gunicorn app:app
   ```

   **Instance Type:** 
   - Select **"Free"** (should be pre-selected)
   - Shows "$0/month"

4. **Scroll Down - Environment Variables**

   Click "Advanced" to expand

   Add these environment variables (click "+ Add Environment Variable" for each):

   | Key | Value |
   |-----|-------|
   | PYTHON_VERSION | 3.11.0 |
   | PORT | 10000 |

5. **Review Settings**
   - Make sure "Free" plan is selected
   - All fields are filled correctly

6. **Deploy!**
   - Click "Create Web Service"
   - Render will start building your app

### Step 3: Wait for Deployment (2-3 minutes)

You'll see a build log with lines like:
```
==> Downloading buildpack...
==> Installing Python 3.11.0
==> Installing dependencies from requirements.txt
==> Build successful!
==> Starting service...
==> Your service is live!
```

**Status indicators:**
- 🟡 Yellow "Building" - Wait...
- 🟢 Green "Live" - Success! ✅

---

## Part 4: Configure Your App URL (1 minute)

### Step 1: Get Your URL

Once deployed (status shows "Live"), you'll see your URL at the top:
```
https://tenant-agent-abc123.onrender.com
```

**Copy this URL!**

### Step 2: Update Property Details

⚠️ **Important:** We need to update the form URL in your app

1. **Go back to GitHub**
   - Navigate to your `tenant-agent` repository
   - Click on `app.py`
   - Click the pencil icon (Edit)

2. **Update the form_url**
   Find this line:
   ```python
   'form_url': 'https://YOUR-APP-NAME.onrender.com/form'
   ```
   
   Replace with YOUR actual Render URL:
   ```python
   'form_url': 'https://tenant-agent-abc123.onrender.com/form'
   ```

3. **Also update your property details** (if you haven't already):
   ```python
   property_details = {
       'address': '123 Main St, Boston, MA 02101',  # ← YOUR address
       'rent': '2200',                               # ← YOUR rent
       'bedrooms': '3',                              # ← YOUR bedrooms
       'bathrooms': '2',                             # ← YOUR bathrooms
       'available_date': 'March 15, 2026',          # ← YOUR date
       'form_url': 'https://tenant-agent-abc123.onrender.com/form'  # ← YOUR URL
   }
   ```

4. **Commit Changes**
   - Scroll down
   - Click "Commit changes"
   - Click "Commit changes" again in the popup

5. **Render Auto-Redeploys**
   - Go back to Render dashboard
   - You'll see it automatically rebuild (takes 1-2 minutes)
   - Wait for "Live" status again

---

## Part 5: Test Your Deployment! (2 minutes)

### Test 1: Basic Check
Visit: `https://YOUR-APP.onrender.com/test`

You should see a success page with links.

### Test 2: View the Form
Visit: `https://YOUR-APP.onrender.com/form`

You should see your beautiful tenant application form with YOUR property details.

### Test 3: Submit a Test Application
1. Fill out the form with fake data
2. Submit it
3. You should see a success page

### Test 4: Check Dashboard
Visit: `https://YOUR-APP.onrender.com/`

You should see the test application you just submitted!

### Test 5: Get Auto-Response
Visit: `https://YOUR-APP.onrender.com/api/auto-response`

You should see JSON with your Facebook Marketplace response message.

---

## 🎉 Success Checklist

- [ ] Render shows "Live" status (green)
- [ ] Test page loads (https://your-app.onrender.com/test)
- [ ] Form displays with YOUR property details
- [ ] Can submit test application
- [ ] Dashboard shows submitted applications
- [ ] Auto-response API returns message

**All checked?** You're live! 🚀

---

## 📱 Using with Facebook Marketplace

Now that you're deployed:

### Step 1: Get Your Auto-Response Message
Visit: `https://YOUR-APP.onrender.com/api/auto-response`

Copy the entire message shown.

### Step 2: Use on Facebook Marketplace

When someone messages you about your property:

1. **Paste the auto-response** as your reply
2. The message includes: `https://YOUR-APP.onrender.com/form`
3. They click the link and fill out the form
4. Check your dashboard at: `https://YOUR-APP.onrender.com/`

**Pro Tip:** Save the auto-response in a note on your phone for quick access!

---

## ⚠️ Important Notes About the Free Tier

### Sleeping Behavior
Your app will:
- **Sleep** after 15 minutes of inactivity
- **Wake up** in 30-50 seconds when someone visits
- This is completely normal for the free tier

**What this means:**
- First visitor after 15+ minutes waits 30-50 seconds
- Subsequent visitors get instant response
- For a rental form, this is perfectly acceptable!

### How to Minimize Wake-Up Time

Add this to your auto-response message on Facebook:
```
The form may take 30 seconds to load on first visit - this is normal! 
Please wait for it to fully load before filling it out.
```

### Keep It Awake (Optional)

If you want the app always ready:

**Option 1: Use a Ping Service (Free)**
- Sign up for https://uptimerobot.com (free)
- Add your URL: `https://YOUR-APP.onrender.com/test`
- Ping every 14 minutes
- This keeps your app awake 24/7

**Option 2: Upgrade to Paid**
- Render paid plan: $7/month
- No sleeping, more resources

---

## 🔒 Security Recommendations

Your app is now public. Here are important security steps:

### 1. Protect Your Dashboard

Add password protection. Update `app.py`:

```python
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("your-secure-password-here")
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

# Add this decorator to protected routes:
@app.route('/')
@auth.login_required
def index():
    # Your dashboard code...
```

Add to `requirements.txt`:
```
Flask-HTTPAuth==4.8.0
```

### 2. Add HTTPS (Already Done!)
Render automatically provides HTTPS. Your app is secure! ✅

### 3. Environment Variables for Sensitive Data

In Render dashboard:
1. Go to your service
2. Click "Environment" tab
3. Add secret variables
4. Use in code: `os.environ.get('SECRET_KEY')`

---

## 🐛 Troubleshooting Guide

### Problem: "Application Error" or "Service Unavailable"

**Check build logs:**
1. Go to Render dashboard
2. Click on your service
3. Click "Logs" tab
4. Look for red error messages

**Common fixes:**
- Make sure all files uploaded to GitHub
- Check `requirements.txt` has gunicorn
- Verify `render.yaml` is present

### Problem: App shows but no styling

**Cause:** CSS not loading

**Fix:** Make sure `templates` folder uploaded correctly to GitHub

### Problem: Forms not submitting

**Check:**
1. Browser console (F12) for errors
2. Render logs for Python errors
3. All required form fields filled

### Problem: Can't see my repo in Render

**Fix:**
1. Click "Configure account" on Render
2. Grant access to your repositories
3. Refresh the page

### Problem: "This site can't be reached"

**Solutions:**
- Wait 2-3 minutes after deployment
- Check Render dashboard shows "Live" status
- Try a different browser
- Check if you typed URL correctly

### Problem: Submissions not appearing in dashboard

**Cause:** Database reset (Render's free tier ephemeral storage)

**Fix:** Use persistent storage:
1. Add PostgreSQL database (free tier available)
2. Or implement database as shown in INTEGRATIONS.md
3. Or accept that data resets on deploys (fine for testing)

---

## 💾 Data Persistence Warning

**Important:** Render's free tier uses ephemeral storage. This means:

❌ `tenant_responses.json` will be deleted when:
- Your app redeploys
- The app restarts
- Render moves your container

### Solutions:

**Option 1: Download Data Regularly**
Add an endpoint to download applications:

```python
@app.route('/download-data')
@auth.login_required
def download_data():
    return send_file('tenant_responses.json', as_attachment=True)
```

Visit `https://YOUR-APP.onrender.com/download-data` to backup

**Option 2: Use a Database (Recommended for Production)**
- Add PostgreSQL (free tier available on Render)
- See INTEGRATIONS.md for SQLite/PostgreSQL setup
- Data persists across restarts

**Option 3: Email Applications to Yourself**
- See INTEGRATIONS.md for email setup
- Each application gets emailed immediately
- No data loss possible

---

## 🔄 Updating Your App

When you want to make changes:

### Method 1: Via GitHub Website
1. Go to your GitHub repo
2. Click on the file to edit
3. Click pencil icon
4. Make changes
5. Commit
6. Render auto-deploys in 2 minutes

### Method 2: Via Git Command Line
```bash
# Make your changes locally
# Then:
git add .
git commit -m "Updated property details"
git push

# Render auto-deploys
```

---

## 📊 Monitoring Your App

### View Logs
1. Go to Render dashboard
2. Click your service
3. Click "Logs" tab
4. See real-time activity

### Check Status
- Dashboard shows if app is running
- Get email alerts if app goes down
- View deploy history

---

## 💰 Cost Summary

| Item | Cost |
|------|------|
| Code | FREE |
| GitHub account | FREE |
| Render hosting | FREE |
| Domain (optional) | FREE (uses .onrender.com) |
| HTTPS/SSL | FREE (included) |
| **Total** | **$0.00/month** |

**Forever free!** No credit card required.

---

## 🎯 Next Steps

Now that you're deployed:

1. **Test thoroughly** with multiple fake applications
2. **Share the form link** on Facebook Marketplace
3. **Add email notifications** (see INTEGRATIONS.md)
4. **Set up UptimeRobot** to keep app awake
5. **Add authentication** to protect dashboard
6. **Consider database** for data persistence

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [GitHub Guides](https://guides.github.com/)

---

## 🆘 Still Stuck?

Common issues and solutions:

**Can't sign up for GitHub?**
- Use email instead of Google/GitHub
- Check spam for verification email

**Repository not showing in Render?**
- Must be public repository
- Configure account permissions in Render

**Build failing?**
- Check all files uploaded
- Verify render.yaml exists
- Check requirements.txt format

**App deployed but not working?**
- Check logs in Render dashboard
- Verify form_url updated in app.py
- Test with /test endpoint first

---

## ✅ Final Checklist

Before going live with real tenants:

- [ ] Test form submission works
- [ ] Dashboard displays applications correctly
- [ ] Property details are accurate
- [ ] Form URL is correct in auto-response
- [ ] Tested on mobile phone
- [ ] Auto-response message saved for easy access
- [ ] Consider adding dashboard password
- [ ] Set up backup/download method for data
- [ ] Optional: Add email notifications
- [ ] Optional: Set up UptimeRobot

---

**Congratulations! Your tenant agent is live and free forever! 🎉**

You now have a professional, automated system for managing Facebook Marketplace property inquiries without spending a cent!
