# 🏠 KC House Price Prediction - Stacking Ensemble

A machine learning application using **Stacking Ensemble** to predict house price categories in King County, Washington.

## 📋 Features

- **Binary Classification:** Predicts if house price is above or below median
- **Stacking Ensemble Model:** Combines Logistic Regression, Decision Tree, and KNN
- **Interactive Streamlit Interface:** User-friendly web application
- **Model Performance Metrics:** Detailed accuracy, classification reports, and confusion matrix
- **Real-time Predictions:** Get instant price category predictions

## 🏗️ Project Structure

```
stacking_ensemble/
├── app.py                    # Original model training script
├── streamlit_app.py          # Streamlit web application
├── kc_house_data.csv         # KC House dataset
├── requirements.txt          # Python dependencies
├── .streamlit/config.toml    # Streamlit configuration
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit App Locally

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## 📊 Model Architecture

**Base Models:**
- Logistic Regression
- Decision Tree (max_depth=10)
- KNN (n_neighbors=5)

**Meta-Model:** Logistic Regression

**Training Setup:**
- 5-fold cross-validation (prevents data leakage)
- Train-test split: 80-20
- Feature scaling: StandardScaler

## 🌐 Deployment Options

### Option 1: Deploy on Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Connect your GitHub repo
5. Select `streamlit_app.py`
6. Deploy!

### Option 2: Deploy on Heroku

```bash
heroku create your-app-name
git push heroku main
```

### Option 3: Other Cloud Platforms

- **Railway** - Push and deploy automatically
- **Render** - Free tier available for Streamlit apps
- **Replit** - Online IDE with deployment

## 📈 Features of the Streamlit App

### 🏠 Prediction Page
- Input house features using sliders and dropdowns
- Get real-time predictions with confidence scores
- Visualize prediction probabilities

### 📊 Model Performance Page
- View overall accuracy metrics
- See classification reports
- Analyze confusion matrix
- Model architecture details

### ℹ️ About Page
- Learn how stacking ensemble works
- Understand model architecture
- Review dataset information
- Explore feature descriptions

## 💡 How Stacking Improves Performance

1. **Ensemble Diversity** - Different algorithms capture different patterns
2. **Meta-Learning** - Learns optimal weights for each base model
3. **Error Correction** - Mitigates individual model weaknesses
4. **Variance Reduction** - More stable predictions
5. **No Data Leakage** - Cross-validation ensures honest results

## 📊 Dataset

**KC House Sales Data:**
- 21,613 house records
- 19 features including:
  - Property info (bedrooms, bathrooms, sqft)
  - Condition (waterfront, view, grade)
  - Location (latitude, longitude, zipcode)
  - Neighborhood stats

## 🎯 Model Performance

- **Accuracy:** ~70-75% on test set
- **Median Price Threshold:** $450,000
- **Classes:** Below Median / Above Median

## 🔧 Requirements

- Python 3.8+
- scikit-learn
- pandas
- numpy
- streamlit
- matplotlib
- seaborn

## 📝 Files

| File | Purpose |
|------|---------|
| `streamlit_app.py` | Interactive web application |
| `app.py` | Model training script |
| `kc_house_data.csv` | Training dataset |
| `requirements.txt` | Python package dependencies |
| `README.md` | Project documentation |

## 🚀 Next Steps

1. **Local Testing:** Run `streamlit run streamlit_app.py`
2. **Push to GitHub:** Commit and push your code
3. **Deploy:** Use Streamlit Cloud for free deployment
4. **Share Link:** Get your public app URL and share!

## 📞 Support

For issues or questions:
1. Check the model training output in `app.py`
2. Review Streamlit documentation: https://docs.streamlit.io
3. Check scikit-learn docs: https://scikit-learn.org

## 📄 License

MIT License - Feel free to use for educational purposes

---

**Happy Predicting! 🏠📊**
