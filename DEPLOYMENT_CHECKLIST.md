# 🚀 Render.com Deployment - Quick Checklist

Print this out and check off each step as you go!

## ✅ Pre-Deployment (5 minutes)

### Files Ready?
- [ ] Downloaded all files from Claude
- [ ] Created `render.yaml` file
- [ ] Updated `requirements.txt` (includes gunicorn)
- [ ] Created `.gitignore` file
- [ ] Updated `app.py` with property details

### Property Details Updated?
Edit `app.py` and fill in:
- [ ] Your property address
- [ ] Monthly rent amount
- [ ] Number of bedrooms
- [ ] Number of bathrooms
- [ ] Available date
- [ ] Form URL (update after deployment)

---

## 📤 GitHub Upload (3 minutes)

### Account Setup
- [ ] Created GitHub account (or logged in)
- [ ] Verified email address

### Repository Created
- [ ] Created new public repository named `tenant-agent`
- [ ] Uploaded all files:
  - [ ] facebook_marketplace_agent.py
  - [ ] app.py
  - [ ] requirements.txt
  - [ ] render.yaml
  - [ ] .gitignore
  - [ ] All .md files
  - [ ] templates/ folder (with 3 HTML files)
- [ ] Verified all files appear on GitHub

---

## 🌐 Render Deployment (5 minutes)

### Account Setup
- [ ] Created Render.com account
- [ ] Connected GitHub account
- [ ] Authorized Render to access repositories

### Service Creation
- [ ] Clicked "New +" → "Web Service"
- [ ] Selected `tenant-agent` repository
- [ ] Configured settings:
  - [ ] Name: `tenant-agent` (or custom name)
  - [ ] Region: Selected
  - [ ] Branch: main
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `gunicorn app:app`
  - [ ] Instance Type: **FREE**
- [ ] Added environment variables:
  - [ ] PYTHON_VERSION = 3.11.0
  - [ ] PORT = 10000

### Deployment Started
- [ ] Clicked "Create Web Service"
- [ ] Watched build logs
- [ ] Status changed to "Live" (green)
- [ ] Copied my app URL: `https://____________.onrender.com`

---

## 🔧 Post-Deployment (2 minutes)

### Update Form URL
- [ ] Went back to GitHub
- [ ] Edited `app.py`
- [ ] Updated `form_url` with my Render URL
- [ ] Committed changes
- [ ] Waited for automatic redeploy
- [ ] Status shows "Live" again

---

## 🧪 Testing (3 minutes)

### Basic Tests
- [ ] Visited: `https://MY-APP.onrender.com/test` ✅
- [ ] Visited: `https://MY-APP.onrender.com/form` ✅
- [ ] Form shows MY property details ✅
- [ ] Submitted test application ✅
- [ ] Saw success page ✅
- [ ] Checked dashboard at: `https://MY-APP.onrender.com/` ✅
- [ ] Test application appears in dashboard ✅

### Auto-Response
- [ ] Visited: `https://MY-APP.onrender.com/api/auto-response`
- [ ] Copied the message
- [ ] Saved it in my phone notes

---

## 📱 Ready to Use!

### For Facebook Marketplace
When someone messages about your property:
1. [ ] Paste auto-response message
2. [ ] They click link and fill out form
3. [ ] Check dashboard for submissions

### My URLs (write them down!)
- **Form:** https://_________________.onrender.com/form
- **Dashboard:** https://_________________.onrender.com/
- **Auto-response:** https://_________________.onrender.com/api/auto-response

---

## 🎯 Optional Enhancements

### Keep App Awake
- [ ] Signed up for UptimeRobot.com
- [ ] Added ping every 14 minutes
- [ ] App stays awake 24/7

### Secure Dashboard
- [ ] Added password protection (see deployment guide)
- [ ] Updated and redeployed

### Email Notifications
- [ ] Set up email alerts (see INTEGRATIONS.md)
- [ ] Tested notification

### Backup Data
- [ ] Added /download-data endpoint
- [ ] Downloading weekly backups

---

## 🐛 If Something Goes Wrong

### Build Failed?
- [ ] Check Render logs for errors
- [ ] Verify all files on GitHub
- [ ] Ensure render.yaml exists
- [ ] Check requirements.txt format

### App Not Loading?
- [ ] Wait 2-3 minutes after deployment
- [ ] Check Status is "Live"
- [ ] Try different browser
- [ ] Check Render logs

### Form Not Working?
- [ ] Verify form_url updated in app.py
- [ ] Check browser console (F12)
- [ ] Look for errors in Render logs

---

## 💾 Important Reminders

⚠️ **Free Tier Limitations:**
- App sleeps after 15 minutes (wakes in 30-50 seconds)
- Data resets on redeploy (use database or download backups)
- 750 free hours/month (enough for 24/7)

✅ **What's Included Free:**
- HTTPS/SSL encryption
- Automatic deploys from GitHub
- Custom .onrender.com subdomain
- Build logs and monitoring

---

## 📞 Support Resources

- **Deployment Guide:** See RENDER_DEPLOYMENT.md
- **App Documentation:** See README.md
- **Advanced Features:** See INTEGRATIONS.md
- **Render Docs:** https://render.com/docs
- **GitHub Help:** https://docs.github.com

---

**Date Deployed:** _______________
**App URL:** _______________
**Status:** ⭐ LIVE AND WORKING!

---

🎉 **Congratulations! You did it!** 🎉

Your tenant application system is now live, professional, and completely free!
