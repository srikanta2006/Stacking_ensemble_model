# 🚀 Deployment Guide - KC House Price Prediction

This guide covers multiple deployment options for your Streamlit application.

---

## 📋 Prerequisites

- Python 3.8+
- Git account
- (Optional) Docker installed
- (Optional) Cloud provider account

---

## Option 1: Streamlit Cloud (Easiest - FREE) ⭐

### Steps:

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Stacking Ensemble ML Model"
   git remote add origin https://github.com/YOUR_USERNAME/kc-house-prediction.git
   git push -u origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit: https://streamlit.io/cloud
   - Click "Sign up with GitHub"
   - Authorize Streamlit

3. **Deploy Application**
   - Click "New app"
   - Select your repository
   - Select branch: `main`
   - Set main file path: `streamlit_app.py`
   - Click "Deploy"

4. **Your app is live!**
   - Get shareable URL like: `https://your-app-name.streamlit.app`
   - Share with anyone!

### Pros:
✅ Free hosting
✅ Automatic updates from GitHub
✅ Easy to manage
✅ Custom domain support (paid)

### Cons:
❌ Limited computing resources
❌ May sleep if inactive

---

## Option 2: Docker + Local Deployment

### Build Image:
```bash
docker build -t kc-house-prediction .
```

### Run Container:
```bash
docker run -p 8501:8501 kc-house-prediction
```

### Or use Docker Compose:
```bash
docker-compose up
```

Access at: `http://localhost:8501`

---

## Option 3: Heroku Deployment

### Prerequisites:
- Heroku account: https://www.heroku.com
- Heroku CLI installed

### Steps:

1. **Create Heroku app**
   ```bash
   heroku login
   heroku create your-app-name
   ```

2. **Deploy**
   ```bash
   git push heroku main
   ```

3. **View logs**
   ```bash
   heroku logs --tail
   ```

Access at: `https://your-app-name.herokuapp.com`

### Cost: Free tier available (limited)

---

## Option 4: AWS EC2 Deployment

### Steps:

1. **Launch EC2 Instance**
   - AMI: Ubuntu 20.04
   - Instance type: t2.micro (free tier eligible)

2. **Connect & Setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python
   sudo apt install python3-pip -y
   
   # Clone repository
   git clone https://github.com/YOUR_USERNAME/kc-house-prediction.git
   cd kc-house-prediction
   
   # Install dependencies
   pip3 install -r requirements.txt
   ```

3. **Run Streamlit**
   ```bash
   streamlit run streamlit_app.py --server.port 80 --server.address 0.0.0.0
   ```

4. **Keep running (using systemd or screen)**
   ```bash
   # Using screen
   screen -S streamlit
   streamlit run streamlit_app.py --server.port 80 --server.address 0.0.0.0
   # Press Ctrl+A then D to detach
   ```

Access at: `http://your-instance-ip`

### Cost: 
- Free tier: 750 hours/month
- Elastic IP: Free (1)

---

## Option 5: Google Cloud Run

### Steps:

1. **Create GCP Project**
   - Go to Google Cloud Console
   - Create new project

2. **Install gcloud CLI**
   ```bash
   # https://cloud.google.com/sdk/docs/install
   ```

3. **Deploy**
   ```bash
   gcloud run deploy kc-house-prediction \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

4. **Get URL** from output

### Cost: Free tier available (generous)

---

## Option 6: Azure App Service

### Steps:

1. **Create Azure Account**: https://azure.microsoft.com

2. **Create Resource Group**
   ```bash
   az group create --name myResourceGroup --location eastus
   ```

3. **Create App Service Plan**
   ```bash
   az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku B1 --is-linux
   ```

4. **Create Web App**
   ```bash
   az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name your-app-name --runtime "PYTHON|3.9"
   ```

5. **Deploy from GitHub**
   - Use continuous deployment from GitHub

Access at: `https://your-app-name.azurewebsites.net`

### Cost: Free tier or paid plans

---

## 📊 Deployment Comparison

| Option | Cost | Ease | Customization | Uptime |
|--------|------|------|---------------|--------|
| Streamlit Cloud | Free | ⭐⭐⭐⭐⭐ | Medium | 99.9% |
| Docker Local | $0 | ⭐⭐⭐ | High | 100% |
| Heroku | Free/Paid | ⭐⭐⭐⭐ | Medium | 99.5% |
| AWS EC2 | Free/Paid | ⭐⭐ | Very High | 99.9% |
| Google Cloud Run | Free/Paid | ⭐⭐⭐ | High | 99.95% |
| Azure App Service | Free/Paid | ⭐⭐⭐ | High | 99.95% |

---

## ✅ Recommended: Streamlit Cloud

**Why?**
- ✅ Completely FREE
- ✅ Takes 5 minutes to deploy
- ✅ Automatic updates from GitHub
- ✅ No infrastructure management
- ✅ Perfect for data science projects
- ✅ Professional looking URL

**How to deploy in 5 minutes:**

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Select your repo and branch
5. Done! 🎉

---

## 🔧 Post-Deployment Tips

### 1. Monitor Your App
- Use platform-specific dashboards
- Monitor performance metrics
- Check error logs regularly

### 2. Update Model
```bash
git add app.py
git commit -m "Updated model"
git push  # Auto-redeploys on Streamlit Cloud
```

### 3. Add Secrets (API keys, passwords)
**For Streamlit Cloud:**
- Dashboard → Settings → Secrets
- Add in format: `KEY = "value"`
- Access in code: `st.secrets["KEY"]`

### 4. Custom Domain (Optional)
- Streamlit Cloud Pro: Connect custom domain
- Other platforms: Use DNS records

### 5. Analytics & Monitoring
- Streamlit Cloud: Built-in analytics
- Others: Use Google Analytics or similar

---

## 📞 Troubleshooting

### Issue: "Module not found"
**Solution:** Add to `requirements.txt` and redeploy

### Issue: "Data file not found"
**Solution:** Ensure `kc_house_data.csv` is in repo root

### Issue: "App crashes on load"
**Solution:** Check logs, look for import errors

### Issue: "Slow predictions"
**Solution:** 
- Increase instance size
- Optimize model loading with `@st.cache_resource`
- Use model compression

---

## 🎓 Learning Resources

- Streamlit Docs: https://docs.streamlit.io
- Deployment Guide: https://docs.streamlit.io/library/deploy
- scikit-learn: https://scikit-learn.org
- Docker: https://www.docker.com

---

## ✨ You're Ready to Deploy!

Choose your preferred option and get started. **Streamlit Cloud is recommended for fastest deployment!**

Happy deploying! 🚀
