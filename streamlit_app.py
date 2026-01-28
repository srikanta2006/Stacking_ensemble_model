import streamlit as st
import pandas as pd
import numpy as np
import pickle
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import StackingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="KC House Price Prediction",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🏠 KC House Price Prediction - Stacking Ensemble")
st.markdown("""
This application uses a **Stacking Ensemble** model to predict whether a house price 
is **above or below the median** price in King County, Washington.

**Model Details:**
- **Base Models:** Logistic Regression, Decision Tree, KNN
- **Meta-Model:** Logistic Regression
- **Task:** Binary Classification (Below/Above Median Price)
""")

# Sidebar for navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Select a page:", ["🏠 Prediction", "📈 Model Performance", "ℹ️ About"])

# Load and prepare data
@st.cache_resource
def load_and_prepare_data():
    """Load data and train models"""
    data = pd.read_csv('./kc_house_data.csv')
    
    # Label encode and one-hot encode categorical features
    le = LabelEncoder()
    data['waterfront'] = le.fit_transform(data['waterfront'])
    data = pd.get_dummies(data, columns=['view', 'condition', 'grade'], drop_first=True)
    
    # Split features and target
    X = data.drop(['id', 'date', 'price'], axis=1)
    median_price = data['price'].median()
    y = (data['price'] > median_price).astype(int)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train stacking model
    base_learners = [
        ('lr', LogisticRegression(max_iter=1000, random_state=42)),
        ('dt', DecisionTreeClassifier(random_state=42, max_depth=10)),
        ('knn', KNeighborsClassifier(n_neighbors=5))
    ]
    
    stacking_model = StackingClassifier(
        estimators=base_learners,
        final_estimator=LogisticRegression(max_iter=1000, random_state=42),
        cv=5
    )
    
    stacking_model.fit(X_train_scaled, y_train)
    
    return data, X, y, X_train_scaled, X_test_scaled, y_train, y_test, stacking_model, scaler, median_price

# Load models
data, X, y, X_train, X_test, y_train, y_test, model, scaler, median_price = load_and_prepare_data()

# Page 1: Prediction
if page == "🏠 Prediction":
    st.header("🔮 Make a Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("House Features")
        
        # Get feature names from training data (excluding the one-hot encoded columns we'll reconstruct)
        feature_cols = X.columns.tolist()
        
        # Create input fields for key features
        bedrooms = st.slider("Bedrooms", 1, 13, 3)
        bathrooms = st.slider("Bathrooms", 0.5, 8.0, 2.0, 0.5)
        sqft_living = st.slider("Living Space (sqft)", 290, 13540, 2000)
        sqft_lot = st.slider("Lot Size (sqft)", 520, 1651359, 5000)
        floors = st.slider("Floors", 1.0, 3.5, 1.5, 0.5)
        waterfront = st.selectbox("Waterfront", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        view = st.selectbox("View Quality", [0, 1, 2, 3, 4])
        condition = st.selectbox("Condition", [1, 2, 3, 4, 5])
        grade = st.selectbox("Building Grade", [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
        sqft_above = st.slider("Square Feet Above Ground", 300, 9410, 1500)
        sqft_basement = st.slider("Square Feet Basement", 0, 4820, 500)
        yr_built = st.slider("Year Built", 1900, 2015, 1990)
        yr_renovated = st.slider("Year Renovated", 0, 2015, 0)
    
    with col2:
        st.subheader("Additional Features")
        
        zipcode = st.number_input("Zip Code", value=98000, step=1)
        lat = st.number_input("Latitude", value=47.5, min_value=47.0, max_value=48.0, step=0.001)
        long = st.number_input("Longitude", value=-122.3, min_value=-122.5, max_value=-121.5, step=0.001)
        sqft_living15 = st.slider("Living Space 15 Neighbors (sqft)", 400, 6210, 1900)
        sqft_lot15 = st.slider("Lot Size 15 Neighbors (sqft)", 651, 871200, 8000)
    
    # Make prediction
    if st.button("🔍 Predict Price Category", key="predict_button"):
        try:
            # Prepare input data
            input_data = pd.DataFrame({
                'bedrooms': [bedrooms],
                'bathrooms': [bathrooms],
                'sqft_living': [sqft_living],
                'sqft_lot': [sqft_lot],
                'floors': [floors],
                'waterfront': [waterfront],
                'view': [view],
                'condition': [condition],
                'grade': [grade],
                'sqft_above': [sqft_above],
                'sqft_basement': [sqft_basement],
                'yr_built': [yr_built],
                'yr_renovated': [yr_renovated],
                'zipcode': [zipcode],
                'lat': [lat],
                'long': [long],
                'sqft_living15': [sqft_living15],
                'sqft_lot15': [sqft_lot15]
            })
            
            # One-hot encode view, condition, grade to match training data
            input_data_encoded = pd.get_dummies(input_data, columns=['view', 'condition', 'grade'], drop_first=True)
            
            # Align with training features
            for col in X.columns:
                if col not in input_data_encoded.columns:
                    input_data_encoded[col] = 0
            
            input_data_encoded = input_data_encoded[X.columns]
            
            # Scale features
            input_scaled = scaler.transform(input_data_encoded)
            
            # Make prediction
            prediction = model.predict(input_scaled)[0]
            prediction_prob = model.predict_proba(input_scaled)[0]
            
            # Display results
            st.success("✅ Prediction Complete!")
            
            result_col1, result_col2 = st.columns(2)
            
            with result_col1:
                if prediction == 1:
                    st.metric(
                        "Price Category",
                        "💰 ABOVE MEDIAN",
                        delta=f"Confidence: {prediction_prob[1]*100:.1f}%"
                    )
                else:
                    st.metric(
                        "Price Category",
                        "💵 BELOW MEDIAN",
                        delta=f"Confidence: {prediction_prob[0]*100:.1f}%"
                    )
            
            with result_col2:
                # Probability chart
                fig, ax = plt.subplots(figsize=(6, 4))
                categories = ['Below Median', 'Above Median']
                probs = prediction_prob
                colors = ['#ff6b6b', '#51cf66']
                ax.barh(categories, probs, color=colors)
                ax.set_xlabel('Probability')
                ax.set_title('Prediction Confidence')
                ax.set_xlim([0, 1])
                
                for i, v in enumerate(probs):
                    ax.text(v + 0.02, i, f'{v*100:.1f}%', va='center')
                
                st.pyplot(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"❌ Error making prediction: {str(e)}")

# Page 2: Model Performance
elif page == "📈 Model Performance":
    st.header("📊 Model Performance Metrics")
    
    # Get predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall Accuracy", f"{accuracy*100:.2f}%")
    
    with col2:
        st.metric("Training Set Size", f"{len(X_train):,} samples")
    
    with col3:
        st.metric("Testing Set Size", f"{len(X_test):,} samples")
    
    # Classification report
    st.subheader("Classification Report")
    class_report = classification_report(y_test, y_pred, target_names=['Below Median', 'Above Median'], output_dict=True)
    report_df = pd.DataFrame(class_report).transpose()
    st.dataframe(report_df, use_container_width=True)
    
    # Confusion Matrix
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Confusion Matrix")
        cm = confusion_matrix(y_test, y_pred)
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                    xticklabels=['Below Median', 'Above Median'],
                    yticklabels=['Below Median', 'Above Median'])
        ax.set_ylabel('True Label')
        ax.set_xlabel('Predicted Label')
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        st.subheader("Model Information")
        st.info(f"""
        **Stacking Ensemble Model**
        
        **Base Models:**
        - Logistic Regression
        - Decision Tree (max_depth=10)
        - KNN (n_neighbors=5)
        
        **Meta-Model:**
        - Logistic Regression
        
        **Cross-Validation:** 5-fold (prevents data leakage)
        
        **Median Price (Threshold):** ${median_price:,.0f}
        """)

# Page 3: About
elif page == "ℹ️ About":
    st.header("About This Model")
    
    st.markdown("""
    ## 🎯 What is Stacking Ensemble?
    
    Stacking is an ensemble learning technique that combines multiple machine learning models 
    to achieve better predictive performance than any single model could achieve alone.
    
    ### How It Works:
    
    1. **Base Models** train on the original training data and make predictions
    2. **Meta-Features** are created from the base models' predictions
    3. **Meta-Model** trains on these meta-features to learn optimal combination weights
    4. **Final Prediction** combines base model predictions via the meta-model
    
    ### Key Advantages:
    
    ✅ **Ensemble Diversity** - Combines different algorithms with different strengths
    
    ✅ **Meta-Learning** - Learns how to weight each base model's predictions
    
    ✅ **Error Correction** - Mitigates individual model weaknesses
    
    ✅ **Variance Reduction** - More stable and robust predictions
    
    ✅ **No Data Leakage** - 5-fold cross-validation ensures honest estimation
    
    ---
    
    ## 📊 Dataset: KC House Sales
    
    - **Location:** King County, Washington
    - **Records:** 21,613 house sales
    - **Features:** 19 house characteristics
    - **Task:** Predict price category (above/below median)
    - **Median Price:** ${:,.0f}
    
    ---
    
    ## 🔧 Model Architecture
    
    ```
    Input Features (17 features)
           ↓
    ┌──────┴──────────┬────────────┬─────────────┐
    ↓                 ↓            ↓             ↓
    Logistic      Decision      KNN (k=5)
    Regression    Tree (d=10)
    ↓             ↓            ↓
    [Predictions from base models]
           ↓
    Meta-Features (3 features)
           ↓
    Logistic Regression (Meta-Model)
           ↓
    Final Classification
    (Below/Above Median)
    ```
    
    ---
    
    ## 📝 Feature List
    
    The model uses the following features for prediction:
    - **Property Info:** bedrooms, bathrooms, sqft_living, sqft_lot, floors
    - **Condition:** waterfront, view, condition, grade
    - **Building:** sqft_above, sqft_basement, yr_built, yr_renovated
    - **Location:** zipcode, latitude, longitude
    - **Neighborhood:** sqft_living15, sqft_lot15
    """.format(median_price))

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🏠 KC House Price Prediction | Stacking Ensemble Model | 2026</p>
</div>
""", unsafe_allow_html=True)
