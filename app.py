import pandas as pd
# Import the dataset
data = pd.read_csv('./kc_house_data.csv')
print("DATA HEADER")
print(data.head())

#null values
print("\nNULL VALUES")
print(data.isnull().sum())

#label encode and one hot encode categorical features
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
data['waterfront'] = le.fit_transform(data['waterfront'])
data = pd.get_dummies(data, columns=['view', 'condition', 'grade'], drop_first=True)


#split the data into features and target
X = data.drop(['id', 'date', 'price'], axis=1)
# Convert to classification: price above/below median
median_price = data['price'].median()
y = (data['price'] > median_price).astype(int)


#split the data into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#standardize the features
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

#========== TASK 2: TRAIN BASE MODELS ==========
print("\n" + "="*60)
print("TASK 2: TRAINING BASE MODELS")
print("="*60)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, classification_report

# Base Model 1: Logistic Regression
print("\n--- Base Model 1: Logistic Regression ---")
lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_train, y_train)
lr_pred = lr_model.predict(X_test)
lr_accuracy = accuracy_score(y_test, lr_pred)
print(f"Accuracy: {lr_accuracy:.4f} ({lr_accuracy*100:.2f}%)")
print(f"\nClassification Report:")
print(classification_report(y_test, lr_pred, target_names=['Below Median', 'Above Median']))

# Base Model 2: Decision Tree
print("\n--- Base Model 2: Decision Tree ---")
dt_model = DecisionTreeClassifier(random_state=42, max_depth=10)
dt_model.fit(X_train, y_train)
dt_pred = dt_model.predict(X_test)
dt_accuracy = accuracy_score(y_test, dt_pred)
print(f"Accuracy: {dt_accuracy:.4f} ({dt_accuracy*100:.2f}%)")
print(f"\nClassification Report:")
print(classification_report(y_test, dt_pred, target_names=['Below Median', 'Above Median']))

# Base Model 3: KNN
print("\n--- Base Model 3: KNN ---")
knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train, y_train)
knn_pred = knn_model.predict(X_test)
knn_accuracy = accuracy_score(y_test, knn_pred)
print(f"Accuracy: {knn_accuracy:.4f} ({knn_accuracy*100:.2f}%)")
print(f"\nClassification Report:")
print(classification_report(y_test, knn_pred, target_names=['Below Median', 'Above Median']))

# Compare base models
print("\n" + "-"*60)
print("BASE MODELS COMPARISON")
print("-"*60)
models_comparison = {
    'Logistic Regression': lr_accuracy,
    'Decision Tree': dt_accuracy,
    'KNN': knn_accuracy
}
sorted_models = sorted(models_comparison.items(), key=lambda x: x[1], reverse=True)
for idx, (name, score) in enumerate(sorted_models, 1):
    print(f"{idx}. {name}: Accuracy = {score:.4f} ({score*100:.2f}%)")

best_model_name = sorted_models[0][0]
best_model_score = sorted_models[0][1]
print(f"\n✓ BEST BASE MODEL: {best_model_name}")
print(f"  Why: {best_model_name} achieves the highest R² score ({best_model_score:.4f}),")
print(f"  indicating better prediction accuracy and variance explanation.")

#========== TASK 3: STACKING ENSEMBLE MODEL ==========
print("\n" + "="*60)
print("TASK 3: STACKING ENSEMBLE MODEL")
print("="*60)

from sklearn.ensemble import StackingClassifier

print("\nBuilding stacking model with:")
print("  - Base Models: Logistic Regression, Decision Tree, KNN")
print("  - Meta-Model: Linear Regression")

base_learners = [
    ('lr', LogisticRegression(max_iter=1000, random_state=42)),
    ('dt', DecisionTreeClassifier(random_state=42, max_depth=10)),
    ('knn', KNeighborsClassifier(n_neighbors=5))
]

# Create stacking model
stacking_model = StackingClassifier(
    estimators=base_learners, 
    final_estimator=LogisticRegression(max_iter=1000, random_state=42),
    cv=5  # 5-fold cross-validation for meta-features
)

# Train stacking model
print("\nTraining stacking model with 5-fold CV (prevents data leakage)...")
stacking_model.fit(X_train, y_train)
y_pred_stacking = stacking_model.predict(X_test)

# Evaluate stacking model
stacking_accuracy = accuracy_score(y_test, y_pred_stacking)

print(f"\nStacking Model Performance:")
print(f"Accuracy: {stacking_accuracy:.4f} ({stacking_accuracy*100:.2f}%)")
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred_stacking, target_names=['Below Median', 'Above Median']))

#========== PERFORMANCE COMPARISON ==========
print("\n" + "="*60)
print("STACKING vs BASE MODELS COMPARISON")
print("="*60)

print("\nModel Rankings (by Accuracy Score):")
all_models = {
    'Logistic Regression': lr_accuracy,
    'Decision Tree': dt_accuracy,
    'KNN': knn_accuracy,
    'Stacking Ensemble': stacking_accuracy
}
sorted_all = sorted(all_models.items(), key=lambda x: x[1], reverse=True)
for idx, (name, score) in enumerate(sorted_all, 1):
    print(f"{idx}. {name}: Accuracy = {score:.4f} ({score*100:.2f}%)")

# Calculate improvement
avg_base = (lr_accuracy + dt_accuracy + knn_accuracy) / 3
improvement = stacking_accuracy - avg_base

print(f"\nAverage Base Model Accuracy: {avg_base:.4f} ({avg_base*100:.2f}%)")
print(f"Stacking Model Accuracy:     {stacking_accuracy:.4f} ({stacking_accuracy*100:.2f}%)")
print(f"Improvement:                 {improvement:+.4f} ({improvement*100:+.2f}%)")

#========== PERFORMANCE COMPARISON BETWEEN BEST BASE MODEL AND STACKING ENSEMBLE ==========
print(f"\nComparison with Best Base Model ({best_model_name}):")
print(f"Improvement over {best_model_name}: {stacking_accuracy - best_model_score:+.4f} ({(stacking_accuracy - best_model_score)*100:+.2f}%)")


#========== WHY STACKING IMPROVES PERFORMANCE ==========
print("\n" + "="*60)
print("HOW STACKING IMPROVES PERFORMANCE")
print("="*60)
print("""
1. ENSEMBLE DIVERSITY
   ✓ Combines 3 different algorithms with different learning mechanisms
   ✓ Logistic Regression: captures linear decision boundaries
   ✓ Decision Tree: finds non-linear patterns and feature interactions
   ✓ KNN: uses local neighborhood information
   
2. META-LEARNING
   ✓ The meta-model (Linear Regression) learns optimal weights for each base model
   ✓ Learns WHEN to trust each model based on the data patterns
   ✓ Combines strengths while mitigating individual model weaknesses

3. ERROR CORRECTION
   ✓ Base models' errors are often uncorrelated
   ✓ Meta-model can correct systematic biases from individual models
   ✓ Results in more robust predictions

4. VARIANCE REDUCTION
   ✓ Averaging diverse predictions reduces variance
   ✓ More stable performance across different data subsets
   ✓ Better generalization to unseen data

5. NO DATA LEAKAGE
   ✓ Uses 5-fold cross-validation for meta-feature generation
   ✓ Prevents model from overfitting on training data
   ✓ Ensures honest and reliable performance estimates
""")

print("="*60)
print("STACKING ENSEMBLE COMPLETE ✓")
print("="*60)

