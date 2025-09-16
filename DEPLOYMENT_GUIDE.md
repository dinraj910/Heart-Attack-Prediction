# 🚀 Free Hosting Deployment Guide

## 🏆 RECOMMENDED: Railway (Best for ML Apps)

Render has compilation issues with scikit-learn. **Railway is now the best option!**

### Step-by-Step Railway Deployment:

1. **🌐 Deploy on Railway**
   ```
   1. Go to https://railway.app
   2. Sign up with GitHub account
   3. Click "New Project" → "Deploy from GitHub repo"
   4. Select your Heart-Attack-Prediction repository
   5. Railway auto-detects Python and uses our railway.toml config
   6. Click "Deploy Now"
   7. Wait 2-3 minutes for build to complete
   ```

2. **⚡ Your website will be live at:**
   ```
   https://[your-app-name].up.railway.app
   ```

3. **💰 Cost**: $5 free credit monthly (more than enough for your app)

---

## � Alternative: PythonAnywhere (Reliable Backup)

### Step-by-Step PythonAnywhere Deployment:

1. **📋 Setup**
   ```
   1. Go to https://www.pythonanywhere.com
   2. Create free account
   3. Go to "Tasks" → "Upload files"
   4. Upload your project ZIP file
   5. Extract in home directory
   6. Go to "Web" tab → "Add new web app"
   7. Choose Flask, Python 3.10
   8. Point to your app.py file
   9. Install packages in Bash console:
      pip3.10 install --user -r requirements.txt
   ```

---

## 🔍 Why Railway Works Better

**Railway Advantages:**
- ✅ **Pre-compiled packages** - No Cython compilation
- ✅ **Better caching** - Faster builds
- ✅ **Docker support** - More reliable deployments  
- ✅ **Automatic HTTPS** - Professional URLs
- ✅ **GitHub integration** - Auto-deploy on push

**Render Issues:**
- ❌ **Compilation required** - scikit-learn build fails
- ❌ **Python 3.13 default** - Compatibility issues
- ❌ **No Docker option** - Limited flexibility

---

## 🐍 Budget Option: PythonAnywhere

### Step-by-Step PythonAnywhere Deployment:

1. **📋 Setup**
   ```
   1. Go to https://www.pythonanywhere.com
   2. Create free account
   3. Upload your project files
   4. Configure web app in Web tab
   5. Set source code path and WSGI file
   ```

---

## 📁 Project Structure (Ready for Deployment)

```
heart-disease-prediction/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── runtime.txt              # Python version
├── Procfile                 # Render/Heroku config
├── railway.json             # Railway config
├── models/
│   └── heart_disease_pipeline.pkl
├── templates/
│   ├── index.html
│   ├── predict.html
│   └── result.html
├── static/
│   ├── style.css
│   ├── animations.js
│   └── print.css
└── README.md
```

---

## 🔍 Troubleshooting

### Common Issues:

#### 1. **Scikit-learn Compilation Error (FIXED!)**
**Error**: `'int_t' is not a type identifier` - Python 3.13 compatibility issue
**Solution**: We've updated to:
- Python 3.11.5 (in runtime.txt)
- Compatible dependency versions (in requirements.txt)

#### 2. **Alternative Solutions if Build Still Fails:**
If you still get build errors, try these files instead:

**Option A: Use requirements-minimal.txt**
```bash
# Rename the file in your repository
mv requirements.txt requirements-backup.txt
mv requirements-minimal.txt requirements.txt
# Then redeploy
```

**Option B: Use Railway instead of Render**
Railway has better build caching and may handle dependencies better.

#### 3. **Other Common Issues:**
1. **Model not loading**: Ensure models/ directory is committed to Git
2. **Dependencies missing**: Check requirements.txt has all packages
3. **Port issues**: App is configured to use environment PORT variable

### Testing Locally:
```bash
pip install -r requirements.txt
python app.py
# Visit: http://localhost:5000
```

---

## 🎯 Post-Deployment Checklist

- [ ] Website loads successfully
- [ ] Homepage displays correctly
- [ ] Prediction form works
- [ ] ML model predictions function
- [ ] Results page shows properly
- [ ] Mobile responsive design works
- [ ] Add live URL to README.md

---

## 💡 Pro Tips

1. **Render** is best for portfolio projects (100% free)
2. **Railway** for more advanced features ($5 credit)
3. **Always test locally** before deploying
4. **Commit all changes** to Git before deployment
5. **Monitor logs** during first deployment

---

Your Heart Disease Prediction AI is now ready for the world! 🌟