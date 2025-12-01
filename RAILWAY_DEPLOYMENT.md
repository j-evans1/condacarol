# 🚂 Railway Deployment Guide for AnacondaClaus

Complete step-by-step guide to deploy AnacondaClaus to Railway with PostgreSQL database.

---

## 📋 Prerequisites

- GitHub account with anacondaclaus repository
- All code pushed to GitHub

---

## 🚀 Deployment Steps

### **Step 1: Create Railway Account**

1. Go to [railway.app](https://railway.app)
2. Click "Login with GitHub"
3. Authorize Railway to access your GitHub repositories
4. Complete signup

### **Step 2: Create New Project**

1. Click "New Project" on Railway dashboard
2. Select "Deploy from GitHub repo"
3. Find and select `anacondaclaus` repository
4. Railway will start creating your project

### **Step 3: Add PostgreSQL Database**

This is crucial! Your app needs a database to store game data.

1. In your project dashboard, click "+ New"
2. Select "Database" → "Add PostgreSQL"
3. Railway will provision a PostgreSQL database
4. Wait for database to be ready (green status)

### **Step 4: Connect Database to App**

Railway automatically creates a `DATABASE_URL` environment variable.

**Verify connection:**
1. Click on your web service (the app)
2. Go to "Variables" tab
3. You should see `DATABASE_URL` listed (Railway adds this automatically)
4. If not visible, the database should still be connected via internal networking

**No manual configuration needed!** Railway handles the connection automatically.

### **Step 5: Configure Deployment**

Your app is already configured via `railway.json`, but verify:

1. Click on your web service
2. Go to "Settings" tab
3. Scroll to "Deploy" section
4. **Start Command** should be:
   ```
   panel serve app.py --address 0.0.0.0 --port $PORT --allow-websocket-origin="*"
   ```
5. **Builder** should be "Nixpacks" (default)

### **Step 6: Generate Domain**

1. Click on your web service
2. Go to "Settings" tab
3. Scroll to "Networking" section
4. Click "Generate Domain"
5. Railway will provide a public URL like: `anacondaclaus.up.railway.app`

### **Step 7: Deploy!**

1. Railway automatically deploys on first setup
2. Watch the "Deployments" tab for build logs
3. Wait for deployment to complete (should take 2-3 minutes)
4. Status will change from "Building" → "Deploying" → "Active"

### **Step 8: Test Your Deployment**

1. Click the generated domain URL
2. You should see the AnacondaClaus login screen
3. Test admin login:
   - Enter admin name
   - Password: `anacondaclaus2024`
   - Create a test city (e.g., "Test City")
4. Open an incognito window and test participant login
5. Select your test city and join

---

## 🎯 Architecture Overview

```
Users (Browsers)
     ↓
Railway Domain (anacondaclaus.up.railway.app)
     ↓
Panel Web App (Your Python app)
     ↓
PostgreSQL Database (Railway-provided)
     ↓
Persistent Storage (Game data, cities, questions, answers, guesses)
```

**Key Features:**
- ✅ **Persistent storage** - Data survives restarts
- ✅ **Shared database** - All users access same data
- ✅ **Real-time updates** - WebSockets work natively
- ✅ **Auto-deploy** - Push to GitHub = auto-deployment
- ✅ **Free tier** - 500 hours/month included

---

## 🔄 Auto-Deployment Setup

Enable automatic deployments when you push to GitHub:

1. Go to your project on Railway
2. Click on your web service
3. Go to "Settings" tab
4. Under "Service" section, verify:
   - **Source**: Your GitHub repo
   - **Branch**: `main`
   - **Auto Deploy**: Should be ON (default)

**Now whenever you push to GitHub, Railway automatically redeploys!**

```bash
# Local development
git add .
git commit -m "Update feature"
git push

# Railway automatically:
# 1. Detects the push
# 2. Pulls latest code
# 3. Rebuilds the app
# 4. Deploys new version
# 5. Zero downtime!
```

---

## 🔧 Environment Variables

Railway automatically provides:

| Variable | Value | Purpose |
|----------|-------|---------|
| `DATABASE_URL` | `postgresql://user:pass@host:5432/db` | PostgreSQL connection |
| `PORT` | Auto-assigned | Web server port |

**No manual configuration needed!**

The app automatically:
- Detects `DATABASE_URL` and uses PostgreSQL
- Falls back to in-memory storage if no database (local dev)

---

## 📊 Monitoring Your Deployment

### **View Logs**

1. Click on your web service
2. Go to "Deployments" tab
3. Click on active deployment
4. View real-time logs

**Useful for:**
- Debugging errors
- Seeing user activity
- Monitoring performance

### **Check Database**

1. Click on PostgreSQL service
2. Go to "Data" tab
3. You can view tables and data directly

**Tables created automatically:**
- `cities` - All cities/offices
- `questions` - Questions per city
- `participants` - Players
- `answers` - User answers
- `guesses` - Game guesses

### **Resource Usage**

1. Go to project dashboard
2. View "Usage" section
3. Monitor:
   - Execution time (500 hours free/month)
   - Database storage
   - Network bandwidth

---

## 🎄 Party Day Checklist

**1 Week Before:**
- [ ] Deploy to Railway
- [ ] Test admin and participant logins
- [ ] Verify database persistence (restart app, data should remain)
- [ ] Share URL with one test user

**1 Day Before:**
- [ ] Create all cities for different offices
- [ ] Prepare 8-12 fun questions
- [ ] Test on mobile devices
- [ ] Send URL to all participants

**Party Day:**
- [ ] Admin logs in and adds questions
- [ ] Start answer phase
- [ ] Participants submit answers
- [ ] Start guessing game
- [ ] View results together!
- [ ] Project results on big screen (optional)

**After Party:**
- [ ] Download screenshots of results (optional)
- [ ] Can delete deployment or leave running for future parties

---

## 🆘 Troubleshooting

### **Issue: App won't start**

**Solution:**
1. Check deployment logs in Railway
2. Look for error messages
3. Common issues:
   - Missing `DATABASE_URL` - verify PostgreSQL service is running
   - Port binding errors - Railway handles this automatically
   - Import errors - verify all dependencies in `requirements.txt`

```bash
# View logs
Railway Dashboard → Your Service → Deployments → Click deployment → View logs
```

### **Issue: Database not connecting**

**Solution:**
1. Verify PostgreSQL service is running (green status)
2. Check that both services are in the same project
3. Railway should automatically link them
4. If not, check "Variables" tab for `DATABASE_URL`

### **Issue: Changes not deploying**

**Solution:**
```bash
# Ensure code is pushed to GitHub
git status
git add .
git commit -m "Your changes"
git push origin main

# Check Railway dashboard
# Should see new deployment triggered automatically
```

### **Issue: WebSocket errors**

**Solution:**
The start command includes `--allow-websocket-origin="*"` which should allow all connections.

If issues persist:
1. Check Railway logs for WebSocket errors
2. Verify the start command in Settings
3. Try regenerating the domain

### **Issue: Data disappearing**

**Solution:**
If using **in-memory storage** (no database), data disappears on restart.

**Fix:**
1. Ensure PostgreSQL service exists in your Railway project
2. Verify `DATABASE_URL` is set
3. Check logs - should see "✅ Database initialized successfully"
4. If you see "⚠️ No DATABASE_URL found", database isn't connected

### **Issue: App is slow**

**Solution:**
- First request after inactivity may be slow (cold start)
- Railway free tier may have some latency
- Consider upgrading to paid tier for better performance
- Database queries should be fast after initial connection

---

## 💰 Pricing

### **Free Tier** (Ideal for party use)

- **500 execution hours/month**
  - ~20 days of 24/7 uptime
  - Perfect for short-term party use
- **PostgreSQL included**
  - 100MB storage (plenty for game data)
- **Shared CPU/RAM**
- **Community support**

**Cost for party:** **$0** ✅

### **Paid Tier** ($5-20/month)

Only needed if:
- Running 24/7 long-term
- Need more than 500 hours/month
- Want dedicated resources
- Need priority support

**For a Christmas party:** Stick with free tier!

---

## 🔐 Security Notes

### **Admin Password**

Default password: `anacondaclaus2024`

**To change:**
1. Edit `app.py` line 393
2. Change `'admin_password': 'anacondaclaus2024'`
3. Push to GitHub (auto-deploys)

**Or use environment variable:**
```python
# In app.py, change to:
'admin_password': os.environ.get('ADMIN_PASSWORD', 'anacondaclaus2024')

# Then in Railway:
# Settings → Variables → Add Variable
# Name: ADMIN_PASSWORD
# Value: your_secret_password
```

### **Data Privacy**

- Data stored in PostgreSQL database
- Only accessible via Railway dashboard (requires login)
- HTTPS enabled automatically
- After party, you can:
  - Delete the project (removes all data)
  - Or keep running for future parties

### **URL Sharing**

- Anyone with URL can access the app
- No authentication required for participants
- Good for parties!
- For more security, add password protection for participants too

---

## 🔄 Updating Your Deployment

### **Method 1: Push to GitHub (Recommended)**

```bash
# Make changes locally
edit app.py

# Commit and push
git add .
git commit -m "Add new feature"
git push

# Railway automatically redeploys!
# Check deployment status in dashboard
```

### **Method 2: Railway Dashboard**

1. Go to project dashboard
2. Click "Deployments"
3. Click "Deploy Latest"
4. Manual redeploy (not recommended)

---

## 🎮 Managing Multiple Parties

### **Same Night, Different Offices**

✅ **Already supported!**
- Each office creates their own city
- Data completely isolated
- All running on same deployment

### **Different Nights/Events**

**Option 1:** Keep existing cities (recommended)
- Each party creates a new city name
- Old data remains for nostalgia

**Option 2:** Clear old data
- Admin can manually clear questions
- Or connect to database and delete old cities

**Option 3:** Fresh start
- Delete and recreate Railway project
- Starts with empty database

---

## 📱 Mobile Access

AnacondaClaus works perfectly on mobile devices!

**Testing:**
1. Open deployment URL on phone
2. Should see responsive design
3. All features work (login, answer, guess, results)

**Tips:**
- Test on both iOS and Android
- Works in all mobile browsers
- No app installation needed
- Share URL via QR code for easy access

---

## 🎉 Success Indicators

Your deployment is successful when:

✅ Domain opens and shows login screen
✅ Admin can create cities and add questions
✅ Participants can select city and join
✅ Answers persist after browser refresh
✅ Multiple users can submit simultaneously
✅ Results show correct scores
✅ Data survives app restarts
✅ Logs show "✅ Database initialized successfully"

---

## 📞 Support

**Railway Issues:**
- Railway Documentation: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

**AnacondaClaus Issues:**
- Check GitHub issues
- Review deployment logs
- Verify database connection

---

## 🎊 You're Ready!

Your AnacondaClaus app is now:
- ✅ Deployed to Railway
- ✅ Connected to PostgreSQL database
- ✅ Accessible via public URL
- ✅ Auto-deploying from GitHub
- ✅ Persistent and reliable
- ✅ Free tier (for party use)

**Share your URL with party participants and have fun!** 🎄🐍🎁
