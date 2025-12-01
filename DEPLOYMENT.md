# 🚀 Deployment Guide for CondaCarol

This guide provides step-by-step instructions for deploying CondaCarol to various platforms.

## 📋 Prerequisites

Before deploying, ensure you have:
- A GitHub account with your code pushed
- The deployment platform account (Heroku, Railway, Render, etc.)

## 🎯 Recommended: Railway (Easiest)

Railway provides free deployments with easy setup:

### Steps:

1. **Sign up at [Railway](https://railway.app/)**
   - Use your GitHub account for easy integration

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `condacarol` repository

3. **Configure**
   - Railway will auto-detect the app
   - It will use the `Procfile` automatically

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete

5. **Get URL**
   - Railway will provide a public URL
   - Share this URL with your party participants!

**Cost**: Free tier available (500 hours/month)

---

## 🟣 Render

Render is another great option with a generous free tier:

### Steps:

1. **Sign up at [Render](https://render.com/)**

2. **New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure**
   - **Name**: `condacarol`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `panel serve app.py --address 0.0.0.0 --port $PORT --allow-websocket-origin="*"`

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment

5. **Access**
   - Use the provided `.onrender.com` URL

**Cost**: Free tier available (spins down after inactivity)

---

## 🟪 Heroku

Classic platform-as-a-service:

### Steps:

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku

   # Or download from heroku.com
   ```

2. **Login**
   ```bash
   heroku login
   ```

3. **Create App**
   ```bash
   cd condacarol
   heroku create your-app-name
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Open**
   ```bash
   heroku open
   ```

**Cost**: Free tier discontinued, starts at $5/month

---

## 🌐 Local Network (Best for Office Parties)

Perfect when everyone is on the same WiFi:

### Steps:

1. **Find Your Local IP**
   ```bash
   # macOS/Linux
   ifconfig | grep "inet " | grep -v 127.0.0.1

   # Windows
   ipconfig
   ```

2. **Start Server**
   ```bash
   conda activate condacarol
   panel serve app.py --address 0.0.0.0 --port 5006 --allow-websocket-origin="*"
   ```

3. **Share URL**
   - Share `http://YOUR-IP:5006` with participants
   - Example: `http://192.168.1.100:5006`

4. **Keep Running**
   - Keep your terminal open during the party
   - Everyone must be on the same network

**Cost**: Free! (requires your computer to stay on)

---

## ☁️ Panel Cloud

Official hosting for Panel apps:

### Steps:

1. **Sign up at [Panel Cloud](https://panel.holoviz.org/)**

2. **Install CLI**
   ```bash
   pip install panel-cloud
   ```

3. **Login**
   ```bash
   panel cloud login
   ```

4. **Deploy**
   ```bash
   cd condacarol
   panel cloud deploy app.py
   ```

**Cost**: Paid service, pricing varies

---

## 🔧 Environment Variables

Some platforms may require environment variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `PORT` | Auto-set | Platform sets this automatically |
| `BOKEH_ALLOW_WS_ORIGIN` | `*` | Allows WebSocket connections |

---

## 📱 Access Control

The app uses a simple password for admin functions:
- Default password: `condaclaus2024`
- To change: Edit `app.py` line 21

For production use, consider:
- Environment variable for password
- More robust authentication
- HTTPS/SSL certificates

---

## 🐛 Common Issues

### Issue: App won't start
**Solution**: Check logs for missing dependencies
```bash
# Heroku
heroku logs --tail

# Railway/Render
Check dashboard logs
```

### Issue: WebSocket errors
**Solution**: Ensure `--allow-websocket-origin="*"` is set

### Issue: Port binding errors
**Solution**: Make sure using `--port $PORT` to use platform's port

### Issue: App times out
**Solution**: Free tiers may have cold starts. First load takes 10-30 seconds.

---

## 🔐 Security Notes

For company parties:
1. **Share URL carefully** - Anyone with the URL can access
2. **Time-limited deployment** - Deploy only during party, delete after
3. **Consider authentication** - Add password protection for non-admin users
4. **Data privacy** - Answers are stored in memory, cleared on restart

---

## 📊 Monitoring

### Check if app is running:
```bash
# Local
curl http://localhost:5006

# Remote
curl https://your-app.railway.app
```

### View active sessions:
- Check server logs for connection counts
- Monitor WebSocket connections

---

## 🎄 Party Day Checklist

- [ ] Deploy app 1 hour before party
- [ ] Test admin password works
- [ ] Add 5-10 questions
- [ ] Send URL to all participants
- [ ] Test on mobile device
- [ ] Have backup plan (screen sharing if deployment fails)
- [ ] Keep laptop/deployment running during party
- [ ] Take screenshots of results!
- [ ] Delete deployment after party (optional, for data privacy)

---

## 💡 Tips

1. **Test deployment early** - Don't wait until party day
2. **Mobile-friendly** - App works on phones and tablets
3. **Screen share** - Project results on a big screen
4. **Backup** - Have local version ready just in case
5. **Questions** - Prepare 8-12 questions for best experience

---

## 🆘 Need Help?

- Check app logs first
- Review platform documentation
- Test locally before deploying
- Open an issue on GitHub

Happy deploying! 🎅🐍🎁
